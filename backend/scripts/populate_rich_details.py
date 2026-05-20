import os
import sys
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables
load_dotenv()

mongo_uri = os.getenv('MONGO_URI') or os.getenv('MONGODB_URI')
if not mongo_uri:
    print("MONGO_URI not found.")
    sys.exit(1)

try:
    client = MongoClient(mongo_uri)
    db_name = 'ethiopian_recommendations'
    if '/' in mongo_uri.replace('mongodb://', '').replace('mongodb+srv://', ''):
        parts = mongo_uri.split('/')
        if parts[-1]:
            db_name = parts[-1].split('?')[0]
    db = client[db_name]
    print(f"Successfully connected to MongoDB database: {db_name}")
except Exception as e:
    print(f"Failed to connect to MongoDB: {e}")
    sys.exit(1)

# Definitions of rich metadata updates for movies, music, and books
rich_data = {
    # MOVIES
    "Teza": {
        "description": "A cinematic masterpiece by Haile Gerima. Teza follows the story of an Ethiopian doctor who returns home during the tumultuous Derg regime, examining the displacement, cultural alienation, and disillusionment of the intellectuals.",
        "description_am": "በሀይሌ ገሪማ የተመራውና የተጻፈው ታላቅ የኢትዮጵያ ፊልም፤ ቴዛ በደርግ ዘመን ወደ ሀገሩ የተመለሰን የኢትዮጵያዊ ሀኪም ህይወትና ምሁራን ያጋጠማቸውን መፈናቀልና ተስፋ መቁረጥ ይተርካል።",
        "cover_image": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=kly6D6qfOaQ"},
            {"provider": "streaming_youtube", "url": "https://www.youtube.com/watch?v=kly6D6qfOaQ"},
            {"provider": "imdb", "url": "https://www.imdb.com/title/1266574/"}
        ]
    },
    "Min Alesh?": {
        "description": "A soulful Ethiopian drama depicting the life, resilience, and struggles of a young female runner from the suburbs of Addis Ababa striving to reach international glory against all odds.",
        "description_am": "ምን አለሽ? በአዲስ አበባ ከተማ ዳርቻ የምትኖር ወጣት ሯጭ ለአለም አቀፍ ዝና ለመብቃት የምታደርገውን የህይወት ትግልና ተጋድሎ የሚያሳይ ልብ የሚነካ የኢትዮጵያ ፊልም ነው።",
        "cover_image": "https://images.unsplash.com/photo-1476480862126-209bfaa8edc8?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=f2iZ8t2bErs"},
            {"provider": "prime_video", "url": "https://www.amazon.com/dp/B08H2HJK4N"}
        ]
    },
    "Sost Maezen": {
        "description": "An epic story tracing the tragic and dangerous lives of East African immigrants crossing borders toward Europe, exploring their harrowing journey, friendship, and the threat of human trafficking.",
        "description_am": "ሶስት ማዕዘን ከምስራቅ አፍሪካ ወደ አውሮፓ የሚሰደዱ ሰዎችን አሰቃቂ ጉዞ፣ ጓደኝነትና የሰዎች ዝውውርን የሚያሳይ እጅግ ልብ የሚነካ የኢትዮጵያ ፊልም ነው።",
        "cover_image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=d_kH4q4Rpy8"},
            {"provider": "streaming_link", "url": "https://www.youtube.com/watch?v=d_kH4q4Rpy8"}
        ]
    },
    "The Shawshank Redemption": {
        "description": "Over the course of several years, two convicts form a friendship, seeking consolation and, eventually, redemption through basic compassion. Directed by Frank Darabont, starring Tim Robbins and Morgan Freeman.",
        "cover_image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=PLl99DlL6b4"},
            {"provider": "netflix", "url": "https://www.netflix.com/title/70005379"},
            {"provider": "hbo_max", "url": "https://www.max.com/movies/shawshank-redemption/e3d81b40-cfc0-4f51-b8ba-9943644fcfc0"}
        ]
    },
    "Inception": {
        "description": "A thief who steals corporate secrets through dream-sharing technology is offered a chance to have his criminal history erased as payment for a seemingly impossible task: 'inception', the implantation of another person's idea into a target's subconscious.",
        "cover_image": "https://images.unsplash.com/photo-1509198397868-475647b2a1e5?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=YoHD9XEInc0"},
            {"provider": "netflix", "url": "https://www.netflix.com/title/70131314"},
            {"provider": "prime_video", "url": "https://www.amazon.com/Inception-Leonardo-DiCaprio/dp/B00471A12Q"}
        ]
    },
    "The Godfather": {
        "description": "The aging patriarch of an organized crime dynasty in postwar New York City transfers control of his clandestine empire to his reluctant youngest son. Widely regarded as one of the greatest films in world cinema.",
        "cover_image": "https://images.unsplash.com/photo-1543536448-d209d2d13a1c?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=UaVTIH8mujA"},
            {"provider": "netflix", "url": "https://www.netflix.com/title/60011152"},
            {"provider": "paramount_plus", "url": "https://www.paramountplus.com/movies/the-godfather/"}
        ]
    },
    "Parasite": {
        "description": "Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan. Winner of 4 Academy Awards, including Best Picture.",
        "cover_image": "https://images.unsplash.com/photo-1594909122845-11baa439b7bf?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=5xH0HfJHsaY"},
            {"provider": "hulu", "url": "https://www.hulu.com/movie/parasite-2fd0b1f6-d183-4a1d-a51b-4f7f2b186b8b"}
        ]
    },
    "Interstellar": {
        "description": "In Earth's future, a global crop blight and second Dust Bowl are slowly rendering the planet uninhabitable. A team of researchers travel through a wormhole in search of a new home for mankind.",
        "cover_image": "https://images.unsplash.com/photo-1451187580459-43490279c0fa?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=zSWdZAToXRw"},
            {"provider": "prime_video", "url": "https://www.amazon.com/Interstellar-Matthew-McConaughey/dp/B00V5D6D50"}
        ]
    },
    "Avatar: The Last Airbender": {
        "description": "A young boy known as the Avatar must master the four elemental powers (Water, Earth, Fire, and Air) to save a world at war — and fight a ruthless Fire Nation enemy bent on absolute global domination.",
        "cover_image": "https://images.unsplash.com/photo-1534447677768-be436bb09401?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_trailer", "url": "https://www.youtube.com/watch?v=waJKJW_XU90"},
            {"provider": "netflix", "url": "https://www.netflix.com/title/81002447"},
            {"provider": "nickelodeon", "url": "https://www.nick.com/shows/avatar-the-last-airbender"}
        ]
    },

    # MUSIC
    "Tizita": {
        "description": "A legendary performance of the iconic Ethiopian pentatonic scale. Tizita represents nostalgia, memory, and sweet longing, acting as the fundamental bedrock of Ethiopian musical heritage.",
        "description_am": "ትውፊታዊው የኢትዮጵያ የትዝታ ቅኝት ሙዚቃ፤ ትዝታ የናፍቆትን፣ የትዝታንና የታሪክን ትውስታ የሚገልጽ የኢትዮጵያ ባህላዊ ሙዚቃ መሰረት ነው።",
        "cover_image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=02fA18B1N7Q"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/62X2gK4qE54k0tFNDgYm3J"}
        ]
    },
    "Bati": {
        "description": "Traditional Bati scale song, expressing soulful cultural storytelling and celebratory folk rhythms native to the Wollo region of Ethiopia.",
        "description_am": "ባህላዊው የባቲ ቅኝት ሙዚቃ፤ በወሎ አካባቢ የሚዘወተርና ልዩ የሆነውን የባህላዊ ዜማና የህዝብ ታሪክ የሚገልጽ ድንቅ ሙዚቃ ነው።",
        "cover_image": "https://images.unsplash.com/photo-1514525253161-7a46d19cd819?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=pYq_g57yY0o"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/4l1O82vB7i4k0tFNDgYm3J"}
        ]
    },
    "Anchihoye Lene": {
        "description": "A classic love ballad utilizing the Anchihoye scale, renowned for its romantic, expressive, and haunting vocal melodies and deep emotional resonance.",
        "description_am": "ልዩ በሆነው የአንቺሆዬ ቅኝት የተሰራ ጥንታዊ የፍቅር ዜማ፤ እጅግ ልብ የሚነካና ስሜትን የሚገልጽ ባህላዊ ሙዚቃ ነው።",
        "cover_image": "https://images.unsplash.com/photo-1487180142328-0c4e37023af5?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=R9YlY8sU-f0"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/5l2O82vB7i4k0tFNDgYm3J"}
        ]
    },
    "Ambassel": {
        "description": "A historic and soulful melody utilizing the Ambassel scale, carrying deep narratives of ancient heroism, nature, regional tales, and highland culture.",
        "description_am": "ጥንታዊውን የአምባሰል ቅኝት መሰረት ያደረገ ታሪካዊ ዜማ፤ ስለ ጀግንነት፣ ተፈጥሮና የደጋማው ማህበረሰብ ባህል የሚተርክ ድንቅ ሙዚቃ ነው።",
        "cover_image": "https://images.unsplash.com/photo-1459749411175-04bf5292ceea?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=1FfR72l7TIE"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/3l2O82vB7i4k0tFNDgYm3J"}
        ]
    },
    "Guramayle": {
        "description": "A beautiful jazz-infused classic Ethiopian piece blending traditional scales with swinging Addis brass instrumentation, popular during the golden age of Ethiopian jazz.",
        "description_am": "በኢትዮ-ጃዝ ወርቃማ ዘመን የተፈጠረና ባህላዊ ቅኝቶችን ከዘመናዊ የነሐስ መሳሪያዎች ጋር ያዋሀደ ድንቅ የግርማ በየነ ሙዚቃ።",
        "cover_image": "https://images.unsplash.com/photo-1511192336575-5a79af67a629?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=uK1XW1p809s"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/2l2O82vB7i4k0tFNDgYm3J"}
        ]
    },
    "One Love": {
        "description": "The timeless reggae anthem promoting peace, unity, and universal love by Bob Marley & The Wailers, widely recognized as a call to global harmony.",
        "cover_image": "https://images.unsplash.com/photo-1482440308425-276ad0f28b19?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=vdB-8eLEW8g"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/2qSkzJcrV42eq6Qj79jQ2a"}
        ]
    },
    "Bohemian Rhapsody": {
        "description": "Queen's epic operatic rock masterpiece, featuring progressive structures, stunning vocal arrangements, and Freddie Mercury's legendary vocal delivery.",
        "cover_image": "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=fJ9rUzIMcZQ"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/7tFkWspUiG55nI42t5wJgA"}
        ]
    },
    "Shape of You": {
        "description": "The record-breaking pop mega-hit with infectious tropical house and dancehall-pop vibes by Ed Sheeran, topping global music charts.",
        "cover_image": "https://images.unsplash.com/photo-1470225620780-dba8ba36b745?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=JGwWNGJdvx8"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/7qiZRhK0hKNmyp21Q56V8g"}
        ]
    },
    "Thriller": {
        "description": "The ultimate pop-disco masterpiece with spooky themes, featuring Michael Jackson's incredible performance and the most iconic, groundbreaking music video in history.",
        "cover_image": "https://images.unsplash.com/photo-1508700115892-45ecd05ae2ad?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "youtube_music", "url": "https://www.youtube.com/watch?v=sOnqjkJTMaA"},
            {"provider": "spotify", "url": "https://open.spotify.com/track/3S26555TYe4G8q64GYY4vO"}
        ]
    },

    # BOOKS (AMHARIC & CLASSICS)
    "Fiker Eske Mekabr": {
        "description": "The most celebrated masterpiece in Amharic literature by Haddis Alemayehu. Fiker Eske Mekabr (Love Unto Grave) is a profound social commentary exploring rigid class struggles, feudalism, and deep romantic tragedy in old Ethiopia.",
        "description_am": "በሐዲስ አለማየሁ የተጻፈው ታላቁና ዝነኛው የኢትዮጵያ ልብ ወለድ መጽሐፍ፤ ፍቅር እስከ መቃብር በባህላዊውና በፊውዳሉ ስርዓት ውስጥ ያሉትን የባላባትና የጭሰኛ መደብ ትግል እንዲሁም ጥልቅ የሆነ የፍቅር ታሪክን ይተርካል።",
        "cover_image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "open_library", "url": "https://openlibrary.org/books/OL26487920M/Fek%CC%A3er_eska_makab%CC%A3er"},
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/15984638-fiqir-isqe-meqabir"}
        ]
    },
    "Sememen": {
        "description": "An award-winning Amharic novel by Sisay Begashaw, capturing the intricate psycho-social landscape, personal relations, and struggles of contemporary Ethiopian urban life.",
        "description_am": "በሲሳይ በጋሻው የተጻፈውና ተወዳጅነትን ያተረፈው ድንቅ መጽሐፍ፤ ሰመመን በዘመናዊ የኢትዮጵያ ከተማ ኑሮ ውስጥ የሚገኙ ማህበራዊ ግንኙነቶችንና የሰዎችን የህይወት ውጣ ውረድ በስሱ ይተርካል።",
        "cover_image": "https://images.unsplash.com/photo-1512820790803-83ca734da794?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/25458097-sememen"}
        ]
    },
    "Alweledim": {
        "description": "A profound philosophical fiction masterpiece by Abe Gubegna. Alweledim (I Will Not Be Born) is a stinging satire and socio-political critique of mid-20th century Ethiopian governance and human rights constraints.",
        "description_am": "በአቤ ጉበኛ የተጻፈው ታላቅ የፍልስፍናና የፖለቲካ መጽሐፍ፤ አልወለድም በ20ኛው ክፍለ ዘመን አጋማሽ የነበረውን የኢትዮጵያን ማህበራዊና ፖለቲካዊ ስርዓት በጠንካራ ምጸት ይተቻል።",
        "cover_image": "https://images.unsplash.com/photo-1543002588-bfa74002ed7e?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/18489728-alweledim"}
        ]
    },
    "To Kill a Mockingbird": {
        "description": "Harper Lee's Pulitzer Prize-winning classic novel exploring severe racial injustice and the destruction of innocence in the American Deep South, narrated by young Scout Finch.",
        "cover_image": "https://images.unsplash.com/photo-1544947950-fa07a98d237f?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "open_library", "url": "https://openlibrary.org/works/OL115797W/To_Kill_a_Mockingbird"},
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/2657.To_Kill_a_Mockingbird"}
        ]
    },
    "1984": {
        "description": "George Orwell's dystopian masterpiece painting a terrifying vision of a totalitarian state under absolute surveillance, censorship, and psychological manipulation controlled by Big Brother.",
        "cover_image": "https://images.unsplash.com/photo-1541963463532-d68292c34b19?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "open_library", "url": "https://openlibrary.org/works/OL1168083W/1984"},
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/40961427-1984"}
        ]
    },
    "The Great Gatsby": {
        "description": "F. Scott Fitzgerald's celebrated novel capturing the excessive luxury, social disillusionment, and personal tragedy of the American jazz age, centered on the enigmatic millionaire Jay Gatsby.",
        "cover_image": "https://images.unsplash.com/photo-1516979187457-637abb4f9353?auto=format&fit=crop&q=80&w=800",
        "links": [
            {"provider": "open_library", "url": "https://openlibrary.org/works/OL468536W/The_Great_Gatsby"},
            {"provider": "goodreads", "url": "https://www.goodreads.com/book/show/77142.The_Great_Gatsby"}
        ]
    }
}

updated_items = 0
added_links = 0

for item in db.items.find():
    title = item.get('title')
    if not title:
        continue
        
    rich_entry = rich_data.get(title)
    if not rich_entry:
        # Check partial match just in case
        for k, v in rich_data.items():
            if k.lower() in title.lower():
                rich_entry = v
                break
                
    if rich_entry:
        update_fields = {}
        # Set description (English and Amharic)
        if rich_entry.get('description'):
            update_fields['description'] = rich_entry['description']
        if rich_entry.get('description_am'):
            update_fields['description_am'] = rich_entry['description_am']
        # Set cover image
        if rich_entry.get('cover_image'):
            update_fields['cover_image'] = rich_entry['cover_image']
            
        if update_fields:
            db.items.update_one({"_id": item["_id"]}, {"$set": update_fields})
            print(f"Updated description & cover for item: {title}")
            updated_items += 1
            
        # Add rich streaming / preview links
        if rich_entry.get('links'):
            for link in rich_entry['links']:
                # Delete existing of the same provider to avoid duplicates
                db.external_links.delete_many({"item_id": item["_id"], "provider": link['provider']})
                # Insert fresh
                db.external_links.insert_one({
                    "item_id": item["_id"],
                    "provider": link['provider'],
                    "url": link['url']
                })
                added_links += 1
            print(f"  -> Added {len(rich_entry['links'])} rich links for: {title}")

print(f"\nDone! Successfully updated rich descriptions for {updated_items} items, and inserted {added_links} high-quality streaming and trailer links!")
