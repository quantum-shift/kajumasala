# kajumasala

## Project Overview
### Inspiration
Struggling to explain tech tasks? Meet FlowPilot-an AI-powered agent that instantly generates step-by-step demos for anything from sending an email to ordering on Amazon. Whether you're a business showcasing a new feature in a sales call or a user learning new tools, our AI makes it effortless. No coding, no confusion—just seamless, interactive demos in seconds!

### What it does
Creates a demo video without any human interference or need. It will explore the product for the task, reason for actions to take, and create a short video recording for you to share! 

### Setup instructions
* Start backend
  ```
  export OPENAI_API_KEY=sk-
  export ELEVENLABS_API_KEY="sk_"
  python main.py
  ```
* Start frontend
  ```
  cd fe_code
  npm install
  npm start
  ```
* Start http server to serve generated demos
  ```
  mkdir output
  cd output
  npm install -g http-server
  http-server ./
  ```
* Now open localhost:3000 on a browser different than chrome
  * This needs to be a different browser due to an issue with playwright + browser_use
* Type your query into the chat box and hit generate!

### How it helps
#### Tech Enablement: 
- Helps students and people with no access to teachers, can easily learn basic tech features using FlowPilot. Do you remember the first time you learnt to send an email? Well FlowPilot makes it a lot more easier, and quicker; enabling more people to learn it
- Have you seen yourself trying to explain a tech feature to your parents on the phone, when you're far away for them? It probably ended with you staying on a call and trying to explain each step. Well FlowPilot will create a quick short video to help share that information

#### Sales Helper:
- When on a sales call, and a customer asks for a new feature; instead of just telling how to do it, now you can send over a video demo for it which can be generated without your manual effort and work. From potential opportunities to sales in seconds 🚀

### How we built it
![image](https://github.com/user-attachments/assets/b3bb7d2b-309d-4d3b-b230-926f8363be9f)

Once the user provides a **"demo description"** and selects a **language**, here's our process:  

1. **Planning the Demo Flow**  
   - Like any intelligent agent, we first create a **high-level demo flow** based on the provided description.  
   - Since we can't generate a demo without understanding the product or feature, we **pre-index relevant resources** such as product documentation, Figma mocks, and other reference materials to guide the agent in designing a structured demo flow.  

2. **Capturing the Demo**  
   - Next, our **"Browser Use" Agent** follows the planned demo flow to **simulate user interactions** and generate a **screen recording** of the product in action.  

3. **Generating Real-time Transcripts**  
   - While the **"Browser Use" Agent** navigates through the product, we simultaneously generate a **natural language transcript** that describes each action being performed, along with helpful explanations to enhance clarity.  

4. **Adding Voice-over with AI**  
   - We then use **Eleven Labs’ Text-2-Speech** to convert the transcript into an **audio narration** in the user’s preferred language.  

5. **Final Assembly: A Seamless Demo Video**  
   - Finally, we synchronize the AI-generated voice-over with the screen recording, creating a **fully polished, engaging demo video**—ready to share! 🚀 

### What we learned

## Team Information
- Naveen LS - Dev
- Udit Desai - Dev + Hypeman :)
- Anubhab Das - Dev
- Kshitiz Bansal - Dev

Equal contribution by all. 

## Compliance
We comply with the hackathons rules and deadlines mentioned here - https://docs.google.com/document/d/17mPGjBrvLAzXP9vjT17q2E8ZYQEH2o-TeZiqDNuaiJk/edit?usp=sharing
