import OpenAI from "openai";
import dotenv from 'dotenv';

dotenv.config();


const modelId = "meta-llama/Llama-2-70b-chat-hf";

const API_URL = `https://api-inference.huggingface.co/models/${modelId}`;

const API_KEY = process.env.HUGGINGFACE_API_KEY;

const openai = new OpenAI({
  baseURL: `${API_URL}/v1/`, // replace with your endpoint url
  apiKey: API_KEY, // replace with your token
});

async function main() {
  const stream = await openai.chat.completions.create({
    model: "meta-llama/Llama-2-70b-chat-hf",
    messages: [
      { role: "system", content: "You are a helpful assistant." },
      { role: "user", content: "Why is open-source software important?" },
    ],
    stream: true,
    max_tokens: 500,
  });
  
  for await (const chunk of stream) {
    process.stdout.write(chunk.choices[0]?.delta?.content || "");
  }
}

main();