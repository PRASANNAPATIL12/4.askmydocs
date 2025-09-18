#!/usr/bin/env python3
"""
Focused DocuBrain Backend Testing
"""

import asyncio
import aiohttp
import json
import uuid
import sys
from pathlib import Path

# Add backend to path for imports
sys.path.append(str(Path(__file__).parent / 'backend'))

# Configuration
BACKEND_URL = "https://askmydocs-backend-yjjs.onrender.com"
API_BASE = f"{BACKEND_URL}/api"

class FocusedTester:
    def __init__(self):
        self.session = None
        self.test_user_token = None
        self.test_user_api_key = None
        self.results = {'passed': 0, 'failed': 0, 'errors': []}
    
    def log_result(self, test_name: str, success: bool, message: str = ""):
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status}: {test_name}")
        if message:
            print(f"   {message}")
        
        if success:
            self.results['passed'] += 1
        else:
            self.results['failed'] += 1
            self.results['errors'].append(f"{test_name}: {message}")
    
    async def setup_session(self):
        timeout = aiohttp.ClientTimeout(total=30)
        self.session = aiohttp.ClientSession(timeout=timeout)
    
    async def cleanup_session(self):
        if self.session:
            await self.session.close()
    
    async def test_root_endpoint(self):
        """Test root endpoint"""
        try:
            async with self.session.get(f"{BACKEND_URL}/") as response:
                if response.status == 200:
                    data = await response.json()
                    if "DocuBrain API is running" in data.get('message', ''):
                        self.log_result("Root Endpoint", True, "API is running")
                        return True
                    else:
                        self.log_result("Root Endpoint", False, f"Unexpected response: {data}")
                        return False
                else:
                    self.log_result("Root Endpoint", False, f"Status: {response.status}")
                    return False
        except Exception as e:
            self.log_result("Root Endpoint", False, f"Exception: {str(e)}")
            return False
    
    async def test_user_registration(self):
        """Test user registration"""
        try:
            username = f"testuser_{uuid.uuid4().hex[:8]}"
            password = "testpass123"
            
            payload = {"username": username, "password": password}
            
            async with self.session.post(f"{API_BASE}/auth/register", json=payload) as response:
                if response.status == 200:
                    data = await response.json()
                    if data.get('success') and data.get('token') and data.get('api_key'):
                        self.test_user_token = data['token']
                        self.test_user_api_key = data['api_key']
                        self.log_result("User Registration", True, f"User created: {username}")
                        return True
                    else:
                        self.log_result("User Registration", False, f"Missing fields: {data}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("User Registration", False, f"Status: {response.status}, Error: {error_text}")
                    return False
        except Exception as e:
            self.log_result("User Registration", False, f"Exception: {str(e)}")
            return False
    
    async def test_text_document_upload(self):
        """Test text document upload"""
        try:
            if not self.test_user_token:
                self.log_result("Text Document Upload", False, "No authentication token")
                return False
            
            headers = {"Authorization": f"Bearer {self.test_user_token}"}
            
            data = aiohttp.FormData()
            data.add_field('title', 'AI Research Document')
            data.add_field('content', 'Artificial intelligence (AI) is a branch of computer science that aims to create intelligent machines capable of performing tasks that typically require human intelligence. Machine learning is a subset of AI that enables computers to learn and make decisions from data without being explicitly programmed for every scenario.')
            
            async with self.session.post(f"{API_BASE}/documents/text", data=data, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('document_id'):
                        self.log_result("Text Document Upload", True, f"Document uploaded: {result['document_id']}")
                        return True
                    else:
                        self.log_result("Text Document Upload", False, f"No document_id: {result}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Text Document Upload", False, f"Status: {response.status}, Error: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Text Document Upload", False, f"Exception: {str(e)}")
            return False
    
    async def test_document_query(self):
        """Test document querying functionality"""
        try:
            if not self.test_user_token:
                self.log_result("Document Query", False, "No authentication token")
                return False
            
            headers = {"Authorization": f"Bearer {self.test_user_token}"}
            query_payload = {"question": "What is artificial intelligence?"}
            
            async with self.session.post(f"{API_BASE}/query", json=query_payload, headers=headers) as response:
                if response.status == 200:
                    result = await response.json()
                    if result.get('answer') and 'sources' in result:
                        answer = result['answer']
                        sources = result['sources']
                        self.log_result("Document Query", True, f"Query successful. Answer: {answer[:100]}...")
                        return True
                    else:
                        self.log_result("Document Query", False, f"Missing answer or sources: {result}")
                        return False
                elif response.status == 400:
                    error_text = await response.text()
                    if "No documents found" in error_text:
                        self.log_result("Document Query", True, "Query endpoint working (no documents as expected)")
                        return True
                    else:
                        self.log_result("Document Query", False, f"Unexpected 400 error: {error_text}")
                        return False
                else:
                    error_text = await response.text()
                    self.log_result("Document Query", False, f"Status: {response.status}, Error: {error_text}")
                    return False
        except Exception as e:
            self.log_result("Document Query", False, f"Exception: {str(e)}")
            return False
    
    async def test_mongodb_integration(self):
        """Test MongoDB integration"""
        try:
            from database import db
            await db.init_db()
            
            test_user_data = {
                "user_id": str(uuid.uuid4()),
                "username": f"dbtest_{uuid.uuid4().hex[:8]}",
                "password": "testpass",
                "api_key": f"sk-test-{uuid.uuid4().hex[:20]}",
                "created_at": "2024-01-01T00:00:00"
            }
            
            success = await db.create_user(test_user_data)
            if not success:
                self.log_result("MongoDB Integration", False, "Failed to create test user")
                return False
            
            retrieved_user = await db.get_user_by_username(test_user_data["username"])
            if not retrieved_user:
                self.log_result("MongoDB Integration", False, "Failed to retrieve test user")
                return False
            
            self.log_result("MongoDB Integration", True, "Database operations successful")
            return True
            
        except Exception as e:
            self.log_result("MongoDB Integration", False, f"Exception: {str(e)}")
            return False
    
    async def test_emergent_llm_integration(self):
        """Test Emergent Universal API integration"""
        try:
            from server import generate_answer_with_emergent_llm
            
            test_question = "What is artificial intelligence?"
            test_context = "Artificial intelligence (AI) is a branch of computer science that aims to create intelligent machines."
            
            response = await generate_answer_with_emergent_llm(test_question, test_context)
            
            if response and not response.startswith("Error generating response"):
                self.log_result("Emergent LLM Integration", True, f"LLM response: {response[:100]}...")
                return True
            else:
                self.log_result("Emergent LLM Integration", False, f"LLM error: {response}")
                return False
                
        except Exception as e:
            self.log_result("Emergent LLM Integration", False, f"Exception: {str(e)}")
            return False
    
    async def run_tests(self):
        """Run focused tests"""
        print("🧠 DocuBrain Backend Testing Suite")
        print("=" * 50)
        
        await self.setup_session()
        
        try:
            tests = [
                ("Root Endpoint", self.test_root_endpoint),
                ("MongoDB Integration", self.test_mongodb_integration),
                ("Emergent LLM Integration", self.test_emergent_llm_integration),
                ("User Registration", self.test_user_registration),
                ("Text Document Upload", self.test_text_document_upload),
                ("Document Query", self.test_document_query),
            ]
            
            for test_name, test_func in tests:
                print(f"\n🔍 Testing: {test_name}")
                await test_func()
            
            # Summary
            print("\n" + "=" * 50)
            print("📊 TEST SUMMARY")
            print("=" * 50)
            print(f"✅ Passed: {self.results['passed']}")
            print(f"❌ Failed: {self.results['failed']}")
            total = self.results['passed'] + self.results['failed']
            if total > 0:
                print(f"📈 Success Rate: {(self.results['passed'] / total * 100):.1f}%")
            
            if self.results['errors']:
                print("\n🚨 FAILED TESTS:")
                for error in self.results['errors']:
                    print(f"   • {error}")
            
            return self.results['failed'] == 0
            
        finally:
            await self.cleanup_session()

async def main():
    tester = FocusedTester()
    success = await tester.run_tests()
    return 0 if success else 1

if __name__ == "__main__":
    exit_code = asyncio.run(main())
    sys.exit(exit_code)