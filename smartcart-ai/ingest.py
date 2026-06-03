import os
import logging
from typing import List, Dict, Any
from dotenv import load_dotenv
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_postgres import PGVector
from langchain_core.documents import Document
import requests
import json

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def fetch_products_from_api() -> List[Dict[str, Any]]:
    """
    Fetch products from Spring Boot API.
    Falls back to sample data if API is not available.
    """
    try:
        response = requests.get("http://localhost:8080/api/products", timeout=5)
        if response.status_code == 200:
            return response.json()
    except Exception as e:
        logger.warning(f"Could not fetch from API: {e}. Using sample data.")
    
    return [
        {
            "id": 101,
            "name": "Acer Aspire 5",
            "category": "laptop",
            "price": 54990,
            "brand": "Acer",
            "desc": "15.6 inch Full HD display laptop with AMD Ryzen 5 processor, 16GB RAM, 512GB SSD, quiet cooling fan, long battery life perfect for students and professionals. Lightweight design with backlit keyboard.",
            "specs": "Ryzen 5 5500U, 16GB DDR4, 512GB NVMe SSD, WiFi 6, Windows 11"
        },
        {
            "id": 102,
            "name": "HP Pavilion 14",
            "category": "laptop",
            "price": 61990,
            "brand": "HP",
            "desc": "Lightweight 14 inch ultrabook with Intel Core i5 processor, excellent keyboard, all-day battery life. Premium aluminum build with fingerprint reader for security.",
            "specs": "Intel i5-1235U, 8GB RAM, 256GB SSD, Iris Xe Graphics, B&O Audio"
        },
        {
            "id": 103,
            "name": "Dell Inspiron 15 3000",
            "category": "laptop",
            "price": 42990,
            "brand": "Dell",
            "desc": "Budget-friendly 15.6 inch laptop for everyday computing, web browsing, and office work. Anti-glare display with comfortable keyboard for long typing sessions.",
            "specs": "Intel i3-1115G4, 8GB RAM, 256GB SSD, HD Webcam, Ubuntu/Windows"
        },
        {
            "id": 104,
            "name": "Lenovo IdeaPad Gaming 3",
            "category": "laptop",
            "price": 74990,
            "brand": "Lenovo",
            "desc": "Entry-level gaming laptop with dedicated NVIDIA graphics, 120Hz display for smooth gaming, RGB keyboard. Ideal for gaming and content creation.",
            "specs": "Ryzen 5 6600H, 16GB RAM, 512GB SSD, RTX 3050, 120Hz FHD"
        },
        {
            "id": 105,
            "name": "ASUS VivoBook 15",
            "category": "laptop",
            "price": 49990,
            "brand": "ASUS",
            "desc": "Stylish and portable 15.6 inch laptop with NanoEdge display, ErgoLift hinge for comfortable typing angle. Great for productivity and entertainment.",
            "specs": "Intel i5-1135G7, 8GB RAM, 512GB SSD, Fingerprint, Windows 11"
        },
        {
            "id": 201,
            "name": "Samsung Galaxy S23",
            "category": "smartphone",
            "price": 74999,
            "brand": "Samsung",
            "desc": "Flagship Android smartphone with triple camera system, 120Hz AMOLED display, all-day battery life. Premium glass and metal design with wireless charging.",
            "specs": "Snapdragon 8 Gen 2, 8GB RAM, 256GB storage, 50MP camera, 5G"
        },
        {
            "id": 202,
            "name": "iPhone 14",
            "category": "smartphone",
            "price": 79900,
            "brand": "Apple",
            "desc": "Premium iOS smartphone with dual camera system, Ceramic Shield front, exceptional battery life. A15 Bionic chip for blazing fast performance.",
            "specs": "A15 Bionic, 6GB RAM, 128GB storage, Dual 12MP cameras, 5G"
        },
        {
            "id": 203,
            "name": "OnePlus 11R",
            "category": "smartphone",
            "price": 39999,
            "brand": "OnePlus",
            "desc": "Fast charging flagship killer with 100W SUPERVOOC charging, smooth 120Hz Fluid AMOLED display. Alert Slider for easy profile switching.",
            "specs": "Snapdragon 8+ Gen 1, 8GB RAM, 128GB UFS 3.1, 50MP IMX890"
        },
        {
            "id": 301,
            "name": "iPad Air",
            "category": "tablet",
            "price": 59900,
            "brand": "Apple",
            "desc": "Powerful tablet with M1 chip, 10.9 inch Liquid Retina display, support for Apple Pencil and Magic Keyboard. Perfect for creativity and productivity.",
            "specs": "M1 chip, 64GB storage, WiFi 6, 12MP cameras, USB-C"
        },
        {
            "id": 302,
            "name": "Samsung Galaxy Tab S8",
            "category": "tablet",
            "price": 55999,
            "brand": "Samsung",
            "desc": "Premium Android tablet with S Pen included, 120Hz display, quad speakers tuned by AKG. DeX mode for desktop-like experience.",
            "specs": "Snapdragon 8 Gen 1, 8GB RAM, 128GB storage, 11 inch LCD"
        },
        {
            "id": 401,
            "name": "Sony WH-1000XM5",
            "category": "headphones",
            "price": 29990,
            "brand": "Sony",
            "desc": "Industry-leading noise canceling headphones with exceptional sound quality, 30-hour battery life. Auto NC optimizer and speak-to-chat technology.",
            "specs": "ANC, Bluetooth 5.2, LDAC, 30hr battery, Multipoint"
        },
        {
            "id": 402,
            "name": "AirPods Pro 2",
            "category": "earbuds",
            "price": 24900,
            "brand": "Apple",
            "desc": "Premium wireless earbuds with active noise cancellation, spatial audio, MagSafe charging case. H2 chip for improved ANC and transparency mode.",
            "specs": "H2 chip, ANC, 6hr + 30hr with case, IPX4, MagSafe"
        },
        {
            "id": 501,
            "name": "Kindle Paperwhite",
            "category": "e-reader",
            "price": 13999,
            "brand": "Amazon",
            "desc": "Waterproof e-reader with 6.8 inch glare-free display, adjustable warm light, weeks of battery life. 8GB storage for thousands of books.",
            "specs": "6.8 inch E-Ink, 300 ppi, IPX8, 8GB, USB-C, 10 weeks battery"
        }
    ]

def create_documents(products: List[Dict[str, Any]]) -> List[Document]:
    """
    Convert product data into LangChain Documents with rich metadata.
    """
    docs = []
    for product in products:
        content_parts = [
            product["name"],
            product.get("brand", ""),
            product["desc"],
            product.get("specs", ""),
            f"Category: {product['category']}",
            f"Price range: {'budget' if product['price'] < 30000 else 'mid-range' if product['price'] < 60000 else 'premium'}"
        ]
        
        page_content = " ".join(filter(None, content_parts))
        
        metadata = {
            "product_id": product["id"],
            "name": product["name"],
            "brand": product.get("brand", "Unknown"),
            "category": product["category"],
            "price": product["price"],
            "price_range": "budget" if product["price"] < 30000 else "mid-range" if product["price"] < 60000 else "premium",
            "description": product["desc"]
        }
        
        docs.append(Document(page_content=page_content, metadata=metadata))
    
    return docs

def ingest_products():
    """
    Main ingestion function that embeds products and stores them in pgvector.
    """
    logger.info("Starting product ingestion...")
    
    products = fetch_products_from_api()
    logger.info(f"Fetched {len(products)} products")
    
    docs = create_documents(products)
    logger.info(f"Created {len(docs)} documents")
    
    logger.info("Initializing HuggingFace embeddings...")
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2",
        model_kwargs={'device': 'cpu'},
        encode_kwargs={'normalize_embeddings': True}
    )
    
    connection_string = os.environ.get("PG_CONN")
    if not connection_string:
        logger.error("PG_CONN environment variable not set!")
        return
    
    logger.info("Connecting to pgvector store...")
    try:
        store = PGVector(
            embeddings=embeddings,
            collection_name="products",
            connection=connection_string,
            use_jsonb=True,
            pre_delete_collection=True  
        )
        
        logger.info("Adding documents to vector store...")
        store.add_documents(docs)
        
        logger.info(f"Successfully indexed {len(docs)} products!")
        
        test_query = "quiet laptop for students"
        logger.info(f"\nTesting retrieval with query: '{test_query}'")
        results = store.similarity_search(test_query, k=3)
        for i, result in enumerate(results, 1):
            logger.info(f"{i}. {result.metadata['name']} - ₹{result.metadata['price']}")
        
    except Exception as e:
        logger.error(f"Error during ingestion: {e}")
        raise

if __name__ == "__main__":
    ingest_products()