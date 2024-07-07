
const OpenAI = require('openai');

const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const fetch = require('node-fetch'); // Import node-fetch library
const axios = require('axios');
const port = 3000;

app.use(bodyParser.json());
app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:5501'],
    credentials: true,
}));
// const openai = new OpenAI({
//     apiKey: "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"// This is also the default, can be omitted
//   });

const {
    GoogleGenerativeAI,
    HarmCategory,
    HarmBlockThreshold,
  } = require("@google/generative-ai");
  
  const apiKey = "AIzaSyCA_8u5iEvnWpHFJtD5WdejRZggqTdvY5s";
  const genAI = new GoogleGenerativeAI(apiKey);
  
  const model = genAI.getGenerativeModel({
    model: "gemini-1.5-flash",
  });
  
  const generationConfig = {
    temperature: 1,
    topP: 0.95,
    topK: 64,
    maxOutputTokens: 8192,
    responseMimeType: "text/plain",
  };
app.post('/query', async (req, res) => {
    const { content } = req.body;

    try {
        const chatSession = model.startChat({
            generationConfig,
         // safetySettings: Adjust safety settings
         // See https://ai.google.dev/gemini-api/docs/safety-settings
            history: [
            ],
          });
        const result = await chatSession.sendMessage(content);
        // console.log(result.response.text());
        const geminiResponse = result.response.text().trim();
        res.json({ content: geminiResponse });
    } catch (error) {
        console.error('Error calling Gemini API:', error);
        res.status(500).json({ error: 'Failed to get response from Gemini API' });
    }
});



// app.post('/query', async (req, res) => {
//     const { content } = req.body;

//     try {
//         const completion = await openai.chat.completions.create({
//             messages: [{ role: "user", content }],
//             model: "gpt-3.5-turbo",
//             max_tokens: 150,
//         });

//         const chatGptResponse = completion.choices[0].message.content.trim();
//         res.json({ content: chatGptResponse });
//     } catch (error) {
//         console.error('Error calling OpenAI API:', error);
//         res.status(500).json({ error: 'Failed to get response from OpenAI API' });
//     }
// });

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});