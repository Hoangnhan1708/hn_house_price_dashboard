
const OpenAI = require('openai');

const express = require('express');
const app = express();
const cors = require('cors');
const bodyParser = require('body-parser');
const fetch = require('node-fetch'); // Import node-fetch library
const port = 3000;

app.use(cors({
    origin: ['http://localhost:3000', 'http://127.0.0.1:5501'],
    credentials: true,
}));
const openai = new OpenAI({
    apiKey: "sk-proj-wJvAt9oSjTO9Y70QR0VXT3BlbkFJoYHmYxktkekH4CM6aB0r"// This is also the default, can be omitted
  });



// Body parser middleware để phân tích cú pháp JSON
app.use(bodyParser.json());



app.post('/query', async (req, res) => {
    const { content } = req.body;

    try {
        const completion = await openai.chat.completions.create({
            messages: [{ role: "user", content }],
            model: "gpt-3.5-turbo",
            max_tokens: 150,
        });

        const chatGptResponse = completion.choices[0].message.content.trim();
        res.json({ content: chatGptResponse });
    } catch (error) {
        console.error('Error calling OpenAI API:', error);
        res.status(500).json({ error: 'Failed to get response from OpenAI API' });
    }
});

app.listen(port, () => {
    console.log(`Example app listening on port ${port}`);
});