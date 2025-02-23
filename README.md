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

### What we learned


## Technical Details -
Public repo - 
[high level design here]

## Team Information
- Naveen LS - Dev
- Udit Desai - Dev + Hypeman :)
- Anubhab Das - Dev
- Kshitiz Bansal - Dev

Equal contribution by all. 

## Compliance
We comply with the hackathons rules and deadlines mentioned here - https://docs.google.com/document/d/17mPGjBrvLAzXP9vjT17q2E8ZYQEH2o-TeZiqDNuaiJk/edit?usp=sharing