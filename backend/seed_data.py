"""
Seed script to populate the database with sample data.
Run this after starting the server for the first time.
"""
import asyncio
import sys
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import AsyncSessionLocal, Bot, ChatSession, Message, Lead
from app.rag.ingestion import document_ingestion
from datetime import datetime, timedelta
import random
import uuid


async def seed_database():
    """Seed the database with sample bot and knowledge base."""
    print("🌱 Starting database seeding...")
    
    async with AsyncSessionLocal() as db:
        try:
            # Create a sample bot
            print("\n📦 Creating sample bot...")
            sample_bot = Bot(
                name="Demo Support Bot",
                system_prompt="""You are a helpful and friendly customer support assistant. 
Your goal is to assist customers with their questions and concerns.
Be polite, professional, and provide accurate information based on the knowledge base.
If you don't know something, be honest and offer to connect them with a human agent.
When appropriate, ask for contact information to follow up.""",
                welcome_message="Hello! 👋 I'm your AI support assistant. How can I help you today?"
            )
            db.add(sample_bot)
            await db.commit()
            await db.refresh(sample_bot)
            print(f"✅ Bot created with ID: {sample_bot.id}")
            
            # Add sample knowledge base content
            print("\n📚 Adding sample knowledge base content...")
            
            sample_documents = [
                {
                    "title": "Company Information",
                    "content": """
About Our Company:
We are a leading provider of AI-powered customer support solutions.
Founded in 2024, our mission is to help businesses provide exceptional customer service 
through intelligent automation.

Contact Information:
- Email: support@example.com
- Phone: 1-800-SUPPORT
- Address: 123 AI Street, Tech City, TC 12345
- Business Hours: Monday-Friday, 9 AM - 6 PM EST

Our Values:
1. Customer First: We prioritize customer satisfaction above all else
2. Innovation: We continuously improve our AI technology
3. Transparency: We believe in honest and open communication
4. Quality: We deliver reliable and accurate solutions
"""
                },
                {
                    "title": "Pricing Information",
                    "content": """
Pricing Plans:

Starter Plan - $49/month
- Up to 1,000 conversations per month
- 1 chatbot
- Email support
- Basic analytics
- 5GB knowledge base storage

Professional Plan - $149/month
- Up to 10,000 conversations per month
- 5 chatbots
- Priority email & chat support
- Advanced analytics
- 50GB knowledge base storage
- Custom branding
- API access

Enterprise Plan - Custom Pricing
- Unlimited conversations
- Unlimited chatbots
- 24/7 dedicated support
- Enterprise analytics
- Unlimited storage
- Custom integrations
- SLA guarantees
- On-premise deployment option

All plans include:
- Free 14-day trial (no credit card required)
- Cancel anytime
- Free setup assistance
- Regular feature updates

Special Offer: Get 20% off annual plans!
"""
                },
                {
                    "title": "Product Features",
                    "content": """
Key Features:

AI-Powered Chat:
- Natural language understanding
- Context-aware conversations
- Multi-language support (20+ languages)
- Sentiment analysis
- Intent detection

Knowledge Management:
- Easy document upload (PDF, TXT, DOC)
- Automatic content indexing
- Semantic search capabilities
- Version control
- Content suggestions

Lead Capture:
- Automatic contact information extraction
- Custom lead forms
- CRM integration (Salesforce, HubSpot, etc.)
- Lead scoring
- Follow-up automation

Analytics & Insights:
- Real-time conversation monitoring
- Customer satisfaction metrics
- Response time tracking
- Popular topics analysis
- Export capabilities (CSV, PDF)

Integrations:
- Website widget (one-line installation)
- Slack
- Microsoft Teams
- WhatsApp
- Facebook Messenger
- Custom API

Security:
- End-to-end encryption
- GDPR compliant
- SOC 2 certified
- Data residency options
- Regular security audits
"""
                },
                {
                    "title": "Getting Started Guide",
                    "content": """
Getting Started with Our Platform:

Step 1: Sign Up
- Visit our website at www.example.com
- Click "Start Free Trial"
- Enter your email and create a password
- Verify your email address

Step 2: Create Your Bot
- Name your bot
- Customize the appearance (colors, logo)
- Write a welcome message
- Set business hours

Step 3: Add Knowledge
- Upload your documentation (FAQs, policies, guides)
- Add product information
- Include contact details
- Review and organize content

Step 4: Train & Test
- Test your bot with sample questions
- Review responses and adjust as needed
- Add more content based on gaps
- Fine-tune system prompts

Step 5: Deploy
- Copy the embed code
- Paste into your website's HTML
- Test on your live site
- Monitor initial conversations

Step 6: Optimize
- Review conversation logs
- Identify common questions
- Add missing information
- Adjust bot personality

Need help? Contact our support team at support@example.com or schedule a demo call!
"""
                },
                {
                    "title": "FAQ",
                    "content": """
Frequently Asked Questions:

Q: How long does setup take?
A: Most customers complete setup in 15-30 minutes. Our team can help if you need assistance.

Q: Do I need technical knowledge?
A: No! Our platform is designed for non-technical users. If you can use email, you can use our platform.

Q: Can I try before buying?
A: Yes! We offer a 14-day free trial with no credit card required.

Q: How accurate is the AI?
A: Our AI achieves 90%+ accuracy on well-documented topics. Accuracy improves as you add more content.

Q: What happens when the bot can't answer?
A: The bot will gracefully hand off to a human agent or capture lead information for follow-up.

Q: Can I customize the bot's appearance?
A: Yes! You can customize colors, logo, position, and welcome message to match your brand.

Q: Is my data secure?
A: Absolutely. We use enterprise-grade encryption and are GDPR & SOC 2 compliant.

Q: Can I cancel anytime?
A: Yes, you can cancel your subscription at any time with no penalties.

Q: Do you offer refunds?
A: Yes, we offer a 30-day money-back guarantee if you're not satisfied.

Q: How do I get support?
A: Email us at support@example.com, use the chat widget on our website, or schedule a call.
"""
                }
            ]
            
            # Ingest each document
            for doc in sample_documents:
                print(f"\n  📄 Ingesting: {doc['title']}")
                
                result = await document_ingestion.ingest_document(
                    content=doc['content'],
                    metadata={
                        "filename": f"{doc['title']}.txt",
                        "source": "seed_data",
                        "title": doc['title']
                    },
                    bot_id=sample_bot.id
                )
                
                if result["success"]:
                    print(f"  ✅ Ingested {result['chunk_count']} chunks")
                else:
                    print(f"  ❌ Failed: {result.get('error', 'Unknown error')}")
            
            print(f"\n✨ Knowledge base seeded!")

            # Add sample sessions and leads
            print("\n👥 Creating sample sessions and leads...")
            
            visitors = [str(uuid.uuid4()) for _ in range(5)]
            sample_leads = [
                {"name": "John Doe", "email": "john@example.com", "phone": "555-0101"},
                {"name": "Jane Smith", "email": "jane@company.com", "phone": None},
                {"name": "Mike Johnson", "email": "mike@tech.co", "phone": "555-0102"}
            ]

            for i, visitor_id in enumerate(visitors):
                # Create session
                session = ChatSession(
                    bot_id=sample_bot.id,
                    visitor_id=visitor_id,
                    created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
                )
                db.add(session)
                await db.flush() # get ID

                # Add messages
                msgs = [
                    Message(session_id=session.id, role="user", content="Hi, what is your pricing?"),
                    Message(session_id=session.id, role="assistant", content="We have three plans: Starter, Professional, and Enterprise. Which one interests you?"),
                    Message(session_id=session.id, role="user", content="Tell me about the Pro plan."),
                ]
                db.add_all(msgs)

                # Add lead to some sessions
                if i < len(sample_leads):
                    lead_data = sample_leads[i]
                    lead = Lead(
                        session_id=session.id,
                        name=lead_data["name"],
                        email=lead_data["email"],
                        phone=lead_data["phone"]
                    )
                    db.add(lead)
            
            await db.commit()
            print("✅ Sample sessions and leads created")

            print(f"\n✨ Seeding complete!")
            print(f"\n🤖 Bot ID: {sample_bot.id}")
            print(f"📝 Bot Name: {sample_bot.name}")
            print(f"\n💡 You can now start the server and test the bot!")
            print(f"   Create a session: POST /api/v1/chat/session")
            print(f"   Connect WebSocket: ws://localhost:8000/ws/chat/{{session_id}}")
            
        except Exception as e:
            print(f"\n❌ Error during seeding: {str(e)}")
            await db.rollback()
            sys.exit(1)


if __name__ == "__main__":
    print("=" * 60)
    print("  AI Customer Support Chatbot - Database Seeder")
    print("=" * 60)
    
    asyncio.run(seed_database())
