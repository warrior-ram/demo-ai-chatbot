"""
Demo response database for pattern-based conversational AI.
Contains pre-defined responses organized by intent categories.
"""
from typing import Dict, List, Any


DEMO_RESPONSES = {
    "greetings": {
        "keywords": ["hello", "hi", "hey", "good morning", "good afternoon", "good evening", "greetings"],
        "responses": [
            "Hello! 👋 How can I assist you today?",
            "Hi there! I'm here to help. What can I do for you?",
            "Hey! Welcome! What brings you here today?",
            "Good day! How may I help you?",
        ],
        "follow_ups": [
            "Is there something specific you'd like to know about?",
            "Feel free to ask me anything!",
        ]
    },
    
    "pricing": {
        "keywords": ["price", "pricing", "cost", "how much", "pay", "payment", "plan", "subscription", "fee"],
        "responses": [
            "Our pricing is designed to fit businesses of all sizes:\n\n"
            "**Starter Plan** - $49/month\n"
            "• Up to 1,000 conversations\n"
            "• 1 chatbot\n"
            "• Email support\n\n"
            "**Professional Plan** - $149/month\n"
            "• Up to 10,000 conversations\n"
            "• 5 chatbots\n"
            "• Priority support\n\n"
            "**Enterprise Plan** - Custom pricing\n"
            "• Unlimited conversations\n"
            "• Dedicated support\n\n"
            "All plans include a 14-day free trial! Which plan interests you?",
            
            "We offer flexible pricing to match your needs! Our plans start at $49/month for small businesses, "
            "with professional ($149/month) and enterprise options available. Would you like details on a specific plan?",
            
            "Great question! We have three tiers:\n"
            "• Starter: $49/month (perfect for getting started)\n"
            "• Pro: $149/month (most popular!)\n"
            "• Enterprise: Custom pricing (for large teams)\n\n"
            "All plans come with a free trial. Interested in trying one?"
        ],
        "follow_ups": [
            "Would you like me to connect you with our sales team?",
            "I can help you choose the right plan. What size is your team?",
            "We also offer a 20% discount on annual plans!",
        ]
    },
    
    "enterprise": {
        "keywords": ["enterprise", "large team", "custom", "unlimited", "dedicated"],
        "responses": [
            "Our Enterprise plan is perfect for larger organizations! It includes:\n"
            "• Unlimited conversations and chatbots\n"
            "• 24/7 dedicated support team\n"
            "• Custom integrations and API access\n"
            "• SLA guarantees\n"
            "• On-premise deployment option\n"
            "• White-label capabilities\n\n"
            "Pricing is customized based on your specific needs. Would you like to speak with our enterprise team?",
            
            "For enterprise customers, we offer custom solutions tailored to your requirements. "
            "This includes unlimited usage, dedicated support, and enterprise-grade security. "
            "I can connect you with our enterprise sales team for a personalized quote. What's the best way to reach you?"
        ]
    },
    
    "features": {
        "keywords": ["feature", "features", "what can", "what does", "how does", "capability", "able to", "functionality"],
        "responses": [
            "Our platform offers powerful features:\n\n"
            "✨ **AI-Powered Chat** - Natural conversations with your customers\n"
            "📚 **Knowledge Base** - Upload documents for instant answers\n"
            "🎯 **Lead Capture** - Automatically collect contact information\n"
            "📊 **Analytics** - Track conversations and satisfaction\n"
            "🔌 **Integrations** - Connect with your existing tools\n"
            "🌐 **Multi-language** - Support 20+ languages\n\n"
            "What would you like to know more about?",
            
            "We've built a comprehensive customer support solution! Key features include real-time chat, "
            "intelligent document search, automatic lead capture, detailed analytics, and seamless integrations "
            "with tools like Slack, Salesforce, and more. What interests you most?"
        ]
    },
    
    "getting_started": {
        "keywords": ["how to start", "get started", "begin", "setup", "install", "implement", "onboard"],
        "responses": [
            "Getting started is super easy! Here's the quick process:\n\n"
            "1️⃣ **Sign up** (takes 2 minutes)\n"
            "2️⃣ **Customize your bot** (name, colors, message)\n"
            "3️⃣ **Add knowledge** (upload FAQs, docs, or paste text)\n"
            "4️⃣ **Test it out** (chat with your bot)\n"
            "5️⃣ **Deploy** (copy embed code to your website)\n\n"
            "The whole process takes about 15-30 minutes. We also offer free setup assistance!",
            
            "Welcome aboard! Setup is straightforward: sign up, create your bot, add your knowledge base content, "
            "test the responses, and then embed it on your site with a single line of code. "
            "Our team can also help you get set up. Would you like a demo?"
        ]
    },
    
    "support": {
        "keywords": ["help", "support", "issue", "problem", "error", "bug", "not working", "broken"],
        "responses": [
            "I'm here to help! Can you tell me more about the issue you're experiencing? "
            "The more details you provide, the better I can assist you.",
            
            "Sorry to hear you're having trouble! Let me help you resolve this. "
            "What specifically isn't working as expected?",
            
            "I'd be happy to help! Could you describe:\n"
            "• What you were trying to do\n"
            "• What happened instead\n"
            "• Any error messages you saw\n\n"
            "This will help me assist you better!"
        ],
        "follow_ups": [
            "If this is urgent, I can connect you with our support team right away.",
            "Have you tried refreshing the page?",
        ]
    },
    
    "contact": {
        "keywords": ["contact", "email", "phone", "call", "reach", "talk to", "speak with", "get in touch"],
        "responses": [
            "You can reach us through several channels:\n\n"
            "📧 **Email**: support@example.com\n"
            "📞 **Phone**: 1-800-SUPPORT\n"
            "💬 **Live Chat**: Right here!\n"
            "🕐 **Hours**: Monday-Friday, 9 AM - 6 PM EST\n\n"
            "Would you like me to have someone from our team reach out to you?",
            
            "I can help connect you with our team! What's the best way to reach you - email or phone? "
            "Or if you prefer, you can email us at support@example.com or call 1-800-SUPPORT.",
        ]
    },
    
    "demo": {
        "keywords": ["demo", "demonstration", "show me", "see it", "trial", "test"],
        "responses": [
            "I'd love to show you what we can do! We offer:\n\n"
            "🆓 **14-day free trial** - No credit card required\n"
            "🎥 **Live demo** - Schedule a call with our team\n"
            "🎮 **Interactive playground** - Test it yourself right now\n\n"
            "Which would you prefer?",
            
            "Great! You can try our platform risk-free with a 14-day trial, or I can schedule a personalized "
            "demo with our team. The demo takes about 30 minutes and we'll show you everything. What works better for you?"
        ]
    },
    
    "integration": {
        "keywords": ["integrate", "integration", "connect", "api", "webhook", "slack", "salesforce", "crm"],
        "responses": [
            "We integrate with all major platforms! Popular integrations include:\n\n"
            "🔗 **CRM**: Salesforce, HubSpot, Pipedrive\n"
            "💬 **Chat**: Slack, Microsoft Teams, Discord\n"
            "📱 **Social**: WhatsApp, Facebook Messenger\n"
            "🛠️ **Custom**: REST API, Webhooks\n\n"
            "What tool are you looking to connect with?",
            
            "Yes! We offer native integrations with popular tools and a full REST API for custom integrations. "
            "Our most used integrations are with CRMs like Salesforce and communication tools like Slack. "
            "What's your tech stack?"
        ]
    },
    
    "security": {
        "keywords": ["security", "secure", "safe", "privacy", "gdpr", "compliance", "data", "encryption"],
        "responses": [
            "Security is our top priority! We provide:\n\n"
            "🔒 **End-to-end encryption** for all data\n"
            "✅ **GDPR compliant** - Full data privacy\n"
            "🏆 **SOC 2 certified** - Enterprise-grade security\n"
            "🌍 **Data residency options** - Store data in your region\n"
            "🔍 **Regular security audits** - Third-party verified\n\n"
            "Your data and your customers' data are completely secure with us.",
            
            "Absolutely! We take security very seriously. All data is encrypted, we're GDPR and SOC 2 compliant, "
            "and we conduct regular security audits. We also offer data residency options for enterprises. "
            "Is there a specific security concern you have?"
        ]
    },
    
    "comparison": {
        "keywords": ["compare", "versus", "vs", "better than", "difference", "alternative", "competitor"],
        "responses": [
            "Great question! What sets us apart:\n\n"
            "✨ **Easier setup** - Most competitors take days, we take 30 minutes\n"
            "🎯 **Better accuracy** - Advanced RAG technology for precise answers\n"
            "💰 **Fair pricing** - No hidden fees, transparent tiers\n"
            "🤝 **Amazing support** - Real humans, quick response times\n"
            "🔧 **Customizable** - Fully white-label capable\n\n"
            "Which aspect matters most to you?",
            
            "We're designed to be the most developer-friendly and business-effective solution. "
            "Unlike many competitors, we focus on accuracy over speed, provide transparent pricing, "
            "and offer actual human support. What specific features are you comparing?"
        ]
    },
    
    "thanks": {
        "keywords": ["thank", "thanks", "appreciate", "helpful", "great"],
        "responses": [
            "You're very welcome! Happy to help! 😊",
            "My pleasure! Is there anything else you'd like to know?",
            "Glad I could help! Feel free to ask if you have more questions.",
            "Anytime! That's what I'm here for! 🎉"
        ]
    },
    
    "goodbye": {
        "keywords": ["bye", "goodbye", "see you", "later", "thanks bye", "gotta go"],
        "responses": [
            "Goodbye! Feel free to come back anytime. Have a great day! 👋",
            "Thanks for chatting! If you need anything else, I'm always here. Take care!",
            "See you later! Don't hesitate to return if you have more questions. Bye! 😊"
        ]
    },
    
    "complaint": {
        "keywords": ["disappointed", "frustrated", "angry", "terrible", "awful", "bad", "worst", "hate"],
        "responses": [
            "I'm really sorry to hear that you're having a negative experience. Your feedback is important to us. "
            "Can you tell me more about what went wrong so I can help make it right?",
            
            "I apologize for the frustration. That's definitely not the experience we want you to have. "
            "Let me connect you with a senior team member who can address this immediately. What's the best way to reach you?",
        ]
    },
    
    "lead_capture": {
        "keywords": ["sign up", "register", "interested", "want to try", "schedule", "book", "meeting"],
        "responses": [
            "Excellent! I'd love to help you get started. What's the best email address to reach you at?",
            "Great! To proceed, I'll need your email address. Then we can set everything up for you.",
            "Perfect! Let me get your contact information so our team can reach out. What's your email?"
        ]
    },
    
    "fallback": {
        "keywords": [],
        "responses": [
            "That's an interesting question! While I process that, could you provide a bit more detail about what you're looking for?",
            "I want to make sure I give you the most accurate information. Could you rephrase that or give me more context?",
            "Great question! Let me connect you with a specialist who can provide detailed information about that. "
            "What's the best way to reach you?",
            "I'm here to help! Can you tell me more about what you need? The more details you provide, the better I can assist.",
            "Interesting! While I'm learning more about that specific topic, is there anything else I can help you with right now?"
        ]
    }
}


# Conversation escalation thresholds
ESCALATION_CONFIG = {
    "max_fallback_count": 3,  # Escalate after 3 fallback responses
    "max_conversation_length": 20,  # Suggest human contact after 20 messages
    "frustration_keywords": ["frustrated", "angry", "terrible", "awful", "useless", "waste"],
}


# Lead capture triggers
LEAD_INTENT_TRIGGERS = [
    "sign up", "register", "interested", "want to try", "schedule", 
    "book", "meeting", "demo", "contact", "reach out", "call me", "email me"
]
