from unittest.mock import patch
import unittest
from ecom_support import EcommerceSupport

class TestEcommerceSupport(unittest.TestCase):
    
    def setUp(self):
        # Mock parameters
        self.chatbot = EcommerceSupport(model_type="gemini", api_key="test-api-key")

    @patch('ecom_support.ConversationChain.predict') 
    def test_order_status_valid_id(self, mock_predict):
        # Mock response
        mock_predict.return_value = "Order ORD123 is currently Delivered (as of 2024-01-15)."
        response = self.chatbot.process_message("What is the status of my order ORD123?")
        self.assertIn("Delivered", response)

    @patch('ecom_support.ConversationChain.predict')
    def test_order_status_invalid_id(self, mock_predict):
        # Mock response
        mock_predict.return_value = "Sorry, I couldn't find that order. Please check the order ID and try again."
        response = self.chatbot.process_message("What is the status of my order ORD999?")
        self.assertIn("couldn't find", response)

    @patch('ecom_support.ConversationChain.predict') 
    def test_return_policy_request(self, mock_predict):
        # Mock response
        mock_predict.return_value = "You can return most items within 30 days of purchase for a full refund."
        response = self.chatbot.process_message("What is your return policy?")
        self.assertIn("30 days of purchase", response)
    
    @patch('ecom_support.ConversationChain.predict')  # Correct target
    def test_human_representative_request(self, mock_predict):
        # Mock response when a user requests a human representative
        mock_predict.return_value = "I'll connect you with a customer service representative. Please provide your full name."
        response = self.chatbot.process_message("I want to speak to a human representative.")
        self.assertIn("Please provide your full name", response)
    

if __name__ == "__main__":
    unittest.main()
