from unittest.mock import patch
import unittest
from ecom_support import EcommerceSupport

class TestEcommerceSupport(unittest.TestCase):
    
    def setUp(self):
        # Mock parameters
        self.chatbot = EcommerceSupport(model_type="gemini", api_key="")


    def test_order_status_valid_id(self):
        response = self.chatbot.process_message("What is the status of my order ORD123 ?")
        self.assertIn("Delivered", response)
        self.assertIn("2024-01-15", response)

    def test_order_status_invalid_id(self):
        # Test invalid order ID query
        response = self.chatbot.process_message("What is the status of my order ORD999?")
        self.assertIn("couldn't find that order", response)

    @patch('ecom_support.ConversationChain.predict') 
    def test_return_policy_request(self, mock_predict):
        # Mock response
        mock_predict.return_value = "You can return most items within 30 days of purchase for a full refund."
        response = self.chatbot.process_message("What is your return policy?")
        self.assertIn("30 days of purchase", response)
    
    @patch('ecom_support.ConversationChain.predict')  
    def test_human_representative_request(self, mock_predict):
        # Mock response when a user requests a human representative
        mock_predict.return_value = "I'll connect you with a customer service representative. Please provide your full name."
        response = self.chatbot.process_message("I want to speak to a human representative.")
        self.assertIn("Please provide your full name", response)
    
    @patch('ecom_support.ConversationChain.predict') 
    def test_no_order_id_provided(self, mock_predict):
     
        mock_predict.return_value = "This response should not be used."

        # Test no order ID in the message
        response = self.chatbot.process_message("What is the status of my order?")
        self.assertIn("couldn't detect a valid order ID", response)

    @patch('ecom_support.ConversationChain.predict')  
    def test_invalid_order_id(self, mock_predict):
       
        mock_predict.return_value = "This response should not be used."

        # Test invalid order ID handling
        response = self.chatbot.process_message("What is the status of my order ORD999?")
        self.assertEqual(response, "Sorry, I couldn't find that order. Please check the order ID and try again.")

if __name__ == "__main__":
    unittest.main()
