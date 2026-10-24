// Test script for Google AI integration
import * as dotenv from 'dotenv';
import { GoogleGenerativeAI } from '@google/generative-ai';

dotenv.config();

// Initialize the API
const googleApiKey = process.env.GOOGLE_API_KEY;
console.log('API key available:', !!googleApiKey);

if (!googleApiKey) {
  console.error('No Google API key found. Please set the GOOGLE_API_KEY environment variable.');
  process.exit(1);
}

const genAI = new GoogleGenerativeAI(googleApiKey);

async function testGoogleAI() {
  try {
    console.log('Testing Google AI connection...');
    
    // Get the model
    // Try a couple of different model names
    let model;
    try {
      console.log('Trying model: gemini-1.5-pro');
      model = genAI.getGenerativeModel({ model: 'gemini-1.5-pro' });
    } catch (e) {
      console.log('Fallback to model: gemini-pro');
      model = genAI.getGenerativeModel({ model: 'gemini-pro' });
    }
    
    // Generate a simple response
    const prompt = 'Write a "Hello, World!" program in JavaScript.';
    console.log(`Sending prompt: "${prompt}"`);
    
    const result = await model.generateContent(prompt);
    const response = result.response;
    const text = response.text();
    
    console.log('\nResponse from Google AI:');
    console.log('------------------------');
    console.log(text);
    console.log('------------------------');
    
    console.log('\nTest completed successfully!');
  } catch (error) {
    console.error('Error testing Google AI:', error);
  }
}

// Run the test
testGoogleAI();