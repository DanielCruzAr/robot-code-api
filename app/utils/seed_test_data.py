from sqlalchemy.orm import Session
from app.config.database import SessionLocal
from app.models.article import Article
from datetime import datetime, timedelta
import random

FIRST_NAMES = [
    "Alice", "Bob", "Charlie", "Diana", "Eve", "Frank", "Grace", "Hank", "Ivy", "Jack", "Karen", "Leo", "Mona", "Nate", "Olivia", "Paul", "Quinn", "Rita", "Sam", "Tina"
]
LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas", "Taylor", "Moore", "Jackson", "Martin"
]
TITLES = [
    "The Rise of AI", "Understanding Quantum Computing", "The Future of Renewable Energy",
    "Advancements in Biotechnology", "Exploring the Deep Sea", "The Human Brain: A Mystery",
    "Space Exploration: Past, Present, Future", "The Impact of Social Media", "Cybersecurity in the Modern Age",
    "The Evolution of Transportation",
    "Climate Change and Its Effects", "The Art of Programming", "Virtual Reality: Beyond Gaming",
    "The Science of Happiness", "Genetic Engineering: Pros and Cons", "The World of Cryptocurrencies",
    "The Psychology of Decision Making", "Nanotechnology: Tiny Solutions",
    "The Role of Big Data", "The Future of Work",
    "The Internet of Things", "Augmented Reality in Everyday Life", "The Ethics of AI",
    "The Power of Machine Learning", "The Digital Divide", "The Future of Education",
    "The Science Behind Sleep", "The Role of Robotics", "The Future of Healthcare",
    "The Impact of 5G Technology", "The Future of Entertainment",
    "The Science of Climate", "The Future of Agriculture", "The Role of Drones",
    "The Future of Smart Cities", "The Science of Nutrition", "The Role of Social Networks",
    "The Future of Retail", "The Science of Exercise", "The Role of Wearables",
    "The Future of Finance", "The Science of Aging", "The Role of Virtual Assistants",
    "The Future of Marketing", "The Science of Memory", "The Role of Cloud Computing",
    "The Future of Journalism", "The Science of Emotions", "The Role of Open Source",
    "The Future of Travel", "The Science of Learning", "The Role of APIs",
    "The Future of Sports", "The Science of Addiction", "The Role of Social Media Influencers",
    "The Future of Food", "The Science of Vision", "The Role of Mobile Apps",
    "The Future of Music", "The Science of Hearing", "The Role of Streaming Services",
    "The Future of Fashion", "The Science of Touch", "The Role of E-commerce",
    "The Future of Real Estate", "The Science of Smell", "The Role of Online Reviews",
    "The Future of Advertising", "The Science of Taste", "The Role of SEO",
    "The Future of Publishing", "The Science of Pain", "The Role of Content Marketing",
    "The Future of Telecommunications", "The Science of Balance", "The Role of Influencer Marketing",
    "The Future of Insurance", "The Science of Reflexes", "The Role of Affiliate Marketing",
    "The Future of Logistics", "The Science of Coordination", "The Role of Email Marketing",
    "The Future of Construction", "The Science of Posture", "The Role of Social Selling",
    "The Future of Mining", "The Science of Strength", "The Role of Video Marketing",
    "The Future of Energy", "The Science of Endurance", "The Role of Podcasting",
    "The Future of Water", "The Science of Flexibility", "The Role of Webinars",
    "The Future of Waste Management", "The Science of Agility", "The Role of Live Streaming"
]
BODY = """
    Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean lacinia congue eros a malesuada. Vivamus scelerisque tortor id nisl lacinia venenatis. Cras aliquam blandit erat, id varius mauris blandit eu. Donec fringilla facilisis blandit. Fusce in pretium magna, eget gravida eros. Vivamus venenatis nisi efficitur pharetra mollis. Etiam mollis molestie ipsum, vitae tincidunt ligula faucibus nec. Sed sodales at ante nec luctus. Vestibulum lobortis venenatis facilisis. Etiam varius odio ut leo fermentum, vel tincidunt ipsum tempor. Suspendisse potenti. Donec erat erat, ornare vitae ullamcorper sit amet, sodales ac ipsum. Vivamus hendrerit enim eget tempor dapibus. Proin egestas est a nisi egestas, at finibus tortor luctus. Fusce tempus libero sed eros posuere, a consectetur odio ornare.

    Donec id diam vitae lorem mattis scelerisque. Duis suscipit magna lacus, viverra molestie dui mollis in. Integer ut posuere libero. Pellentesque vitae ex aliquam, interdum ante sit amet, tincidunt lectus. Pellentesque augue ligula, egestas a tristique et, tincidunt quis neque. Quisque rutrum leo odio, sed commodo nisl dapibus ac. Praesent commodo nibh pellentesque fermentum posuere. Quisque nec ex interdum, tristique massa vel, consequat nunc. Nulla sit amet semper lorem.

    Nunc urna odio, laoreet commodo luctus feugiat, aliquet non leo. Aenean efficitur massa porta diam facilisis, eu hendrerit lacus blandit. Etiam sed est neque. Praesent ullamcorper sem ac massa egestas tempor. Vestibulum eleifend tincidunt tellus, a rutrum orci imperdiet tempus. Aenean ultrices condimentum elit, sed posuere leo fermentum nec. Nam iaculis sodales lacus, sit amet feugiat dolor pharetra nec. Aliquam pellentesque, augue at posuere maximus, neque libero faucibus quam, vitae dignissim est purus quis ligula. Aenean aliquam lacinia leo eu rhoncus. Etiam ac aliquet nisi. Phasellus placerat ultricies arcu, non faucibus eros.

    Vivamus lectus nulla, venenatis non pretium in, eleifend ut risus. Aenean eget nibh vitae elit luctus commodo. Suspendisse eu mi pulvinar eros consectetur suscipit mollis ut nulla. In aliquet dui urna, semper faucibus mi tincidunt eu. Morbi mollis nisl sollicitudin sapien rutrum, ut cursus erat porttitor. Suspendisse condimentum finibus orci. Donec ultrices eu est eu efficitur. Curabitur varius efficitur egestas.

    Integer tincidunt malesuada velit. Duis condimentum dictum fermentum. Vestibulum rutrum vestibulum metus, sed imperdiet dolor posuere at. Morbi libero odio, luctus vitae tempor vitae, rhoncus a ex. Aliquam nec commodo dui. Ut finibus velit vitae urna suscipit convallis. Nulla facilisi. Curabitur elementum dolor ut est vehicula dictum. Morbi imperdiet nisi nulla, non lacinia nibh vestibulum ut. Cras non volutpat lacus, eu volutpat metus. Proin tristique gravida pulvinar. Quisque non ornare sapien, in feugiat leo.

    In hac habitasse platea dictumst. Nulla sit amet quam enim. Curabitur rhoncus nisi vitae viverra tempor. Cras consequat felis sed fermentum scelerisque. Curabitur sollicitudin maximus lacus, at cursus tortor sagittis eget. Suspendisse pharetra elementum posuere. Vestibulum dignissim laoreet ante quis maximus. Aliquam mattis porta laoreet. Vivamus dignissim mi et turpis finibus, ac porttitor nunc cursus.

    Aliquam et diam id dui pulvinar sodales ac at turpis. Sed elit nibh, volutpat at imperdiet a, pellentesque sed lectus. Cras a malesuada ante. Ut quis elit rutrum dui gravida sollicitudin sit amet quis ex. Nunc sem metus, elementum nec diam ornare, tempus placerat velit. Phasellus varius, arcu a semper scelerisque, urna nisi dictum est, et lacinia nibh diam nec lectus. Aliquam at dolor efficitur, elementum elit non, pharetra metus. In aliquet ex non ligula scelerisque, eget sodales ipsum condimentum. Cras porta eleifend ipsum at lobortis. Phasellus aliquet placerat ligula, a porttitor mauris sodales sed. Sed eleifend lorem at facilisis pellentesque.

    Phasellus a neque odio. Donec laoreet sodales dolor. Etiam dolor justo, sodales at commodo nec, fermentum et leo. Aliquam ac enim sit amet nulla dictum ultricies. Mauris vehicula vehicula nisl, id consequat tellus bibendum at. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed vulputate eros quis libero vehicula efficitur. Pellentesque lobortis vulputate erat, vitae condimentum urna rhoncus et. Nulla ut leo et felis suscipit interdum venenatis nec ipsum. In vel velit ligula.

    Aenean interdum malesuada lorem eu sodales. Cras non justo vel sem molestie pellentesque sit amet eu nisi. Fusce quis dignissim nisi, in ornare purus. In ultrices fringilla dignissim. Etiam dolor leo, faucibus semper risus vel, mollis ornare neque. Donec in risus tempor, mattis ipsum non, auctor nibh. Sed consequat, augue in suscipit commodo, nisl ex aliquam nulla, ac consectetur elit lorem eu risus. Nullam ac lobortis lectus. Etiam eu neque et ante feugiat scelerisque id quis augue. Integer diam ipsum, faucibus quis accumsan eu, consectetur ut dui. Quisque efficitur leo vitae nibh ullamcorper, sed cursus mi sagittis. Aliquam cursus ac enim varius malesuada. Sed massa dolor, dictum facilisis tincidunt eu, laoreet non nunc. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia curae;

    Cras vestibulum efficitur odio, eget sollicitudin sapien egestas cursus. Phasellus scelerisque orci non magna fringilla, vel accumsan lectus viverra. Vestibulum viverra porta leo, non egestas nisl tempus ut. Curabitur eget nunc eu lectus iaculis facilisis vitae nec enim. In hac habitasse platea dictumst. Etiam hendrerit ante sit amet pulvinar elementum. Pellentesque suscipit in nunc id efficitur. Donec vitae nunc magna. Donec et lacinia nulla. Sed a nunc turpis. 
"""
TAGS = [
    ["technology", "ai"], ["science", "quantum"], ["energy", "renewable"],
    ["biotech", "health"], ["ocean", "exploration"], ["neuroscience", "brain"],
    ["space", "astronomy"], ["social media", "society"], ["cybersecurity", "tech"],
    ["transportation", "innovation"]
]


def seed():
    db: Session = SessionLocal()

    # Skip seeding if data already exists
    if db.query(Article).first():
        print("✅ Test data already exists, skipping...")
        db.close()
        return
    
    used_titles = {}

    for _ in range(100):
        author = f"{random.choice(FIRST_NAMES)} {random.choice(LAST_NAMES)}"
        if author not in used_titles:
            used_titles[author] = set()

        available_titles = [t for t in TITLES if t not in used_titles[author]]
        if not available_titles:
            # If all titles used for this author, reset their set
            used_titles[author] = set()
            available_titles = TITLES.copy()

        title = random.choice(available_titles)
        used_titles[author].add(title)

        body_start = random.randint(0, max(0, len(BODY) - 500))
        body_length = random.randint(300, 800)
        body = BODY[body_start:body_start + body_length]
        tags = random.choice(TAGS)
        published_at = datetime.now() - timedelta(days=random.randint(0, 365))

        article = Article(
            author=author,
            title=title,
            body=body,
            tags=tags,
            published_at=published_at
        )
        db.add(article)
    db.commit()
    db.close()
    print("✅ Seeded 100 test articles.")


if __name__ == "__main__":
    seed()
