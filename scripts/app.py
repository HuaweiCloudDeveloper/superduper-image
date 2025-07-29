import json
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from superduper.base.document import Document
# 初始化模型
model = SentenceTransformer('/home/model/all-MiniLM-L6-v2')  

def encode_single(x):
    return model.encode(x, convert_to_numpy=True).tolist()

def encode(x, *args, **kwargs):
    return encode_single([x])[0]

class Collection:
    def __init__(self, db, identifier):
        self.db = db
        self.identifier = identifier

    def insert(self, data):
        return InsertOperation(self.db, self.identifier, data)

    def like(self, query_vector, field, n=3):
        # 执行向量搜索
        results = self.db.client.query_points(
            collection_name=self.identifier,
            query=query_vector,
            limit=n,
        )

        def parse_payload(payload):
            if isinstance(payload, dict):
                return payload
            elif isinstance(payload, str):
                try:
                    # 尝试标准解析
                    return json.loads(payload)
                except json.JSONDecodeError:
                    # 替换单引号后再次尝试
                    fixed = payload.replace("'", '"')
                    try:
                        return json.loads(fixed)
                    except json.JSONDecodeError:
                        print(f"❌ Failed to fix payload: {payload}")
                        return {"error": "failed to decode payload", "raw": payload}
            else:
                print(f"❓ Unknown payload type: {type(payload)}")
                return {"error": "unknown payload type", "raw": str(payload)}

        # 修复：正确处理 ScoredPoint 对象
        return [Document(parse_payload(point.payload)) for point in results.points]

class QdrantDatalayer:
    def __init__(self, client: QdrantClient):
        self.client = client
        self.models = {}  # 存储 superduper 模型

    def add(self, model):
        self.models[model.identifier] = model

    def __getitem__(self, collection_name):
        return Collection(self, collection_name)

    def list_collections(self):
        collections = self.client.get_collections().collections
        return [c.name for c in collections]

    def drop_collection(self, collection_name):
        if self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name)

    def create_collection(self, collection_name, vector_size=384):
        if self.client.collection_exists(collection_name):
            self.client.delete_collection(collection_name)
        self.client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

class InsertOperation:
    def __init__(self, db, collection_name, data):
        self.db = db
        self.collection_name = collection_name
        self.data = data

    def execute(self, model, field):
        if not isinstance(self.data, list) or not all(isinstance(item, dict) for item in self.data):
            raise ValueError("data must be a list of dictionaries")
        points = []
        for idx, item in enumerate(self.data):
            print(f" Inserting item: {item}")
            vector = model.predict(item[field]) if hasattr(model, 'predict') else encode(item[field])
            point = PointStruct(
                id=idx + 1,
                vector=vector,
                payload=item,
            )
            points.append(point)
        print(" Type of payload[0]:", type(points[0].payload))
        print(" Sample payload:", points[0].payload)
        self.db.client.upsert(collection_name=self.collection_name, points=points)
        return len(points)

# 初始化 Qdrant 客户端
client = QdrantClient(url="http://localhost:6333")
# 初始化数据层
datalayer = QdrantDatalayer(client=client)
# 创建集合（可选）
datalayer.create_collection("cities", vector_size=384)
# 定义 SuperDuper Model（兼容性处理）
try:
    from superduper.components.model import Model
    text_encoder = Model(
        identifier='text-encoder',
        predictor=lambda x: encode(x),
        output_schema={'vector': 'array[float32][384]'},
        batch_predict=False,
    )
except TypeError:
    class CustomModel:
        identifier = 'text-encoder'
        def predict(self, x):
            return encode(x)
    text_encoder = CustomModel()
# 添加模型到数据层
datalayer.add(text_encoder)
# 准备数据（必须是 list of dicts）
data = [
    {"city": "Berlin", "description": "Capital of Germany"},
    {"city": "London", "description": "Capital of the UK"},
    {"city": "Beijing", "description": "Capital of China"},
    {"city": "Paris", "description": "Capital of France"},
]
# 插入数据
datalayer['cities'].insert(data).execute(model=text_encoder, field='description')
print("✅ Data inserted into Qdrant via SuperDuperDB")
# 执行向量搜索
query = "A large city in Asia"
vector = encode(query)
results = datalayer['cities'].like(query_vector=vector, field='description', n=3)
print("\n🔍 Search Results:")
for r in results:
    print("📄 Raw Document:", r)
    city = r.get('city', '<missing>')
    description = r.get('description', '<missing>')
    print(f"City: {city}, Description: {description}")
