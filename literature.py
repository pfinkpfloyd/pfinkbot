class Literature:
    def __init__(self, name: str, url: str):
        self.name = name
        self.url = url


literature_options = [
    Literature('IP #1 (Who, What, How, and Why)', 'https://na.org/wp-content/uploads/2024/05/EN3101-IP-1-English.pdf'),
    Literature('IP #2 (The Group)', 'https://na.org/wp-content/uploads/2024/05/EN3102-IP-2-English.pdf'),
    Literature('IP #5 (Another Look)', 'https://na.org/wp-content/uploads/2024/05/3105_Another-Look-IP-5-English.pdf'),
    Literature('IP #6 (Recovery & Relapse)',
               'https://na.org/wp-content/uploads/2024/05/3106_Recovery-Relapse-IP-6-English.pdf'),
    Literature('IP #7 (Am I an Addict?)', 'https://na.org/wp-content/uploads/2024/05/EN3107-IP-7-English.pdf'),
    Literature('IP #8 (Just for Today)',
               'https://na.org/wp-content/uploads/2024/05/3108_Just-for-Today-IP-8-English.pdf'),
    Literature('IP #9 (Living the Program)', 'https://na.org/wp-content/uploads/2024/05/EN3109-IP-9-English.pdf'),
    Literature('IP #11 (Sponsorship)', 'https://na.org/wp-content/uploads/2024/05/3111_Sponsorship-IP-11-English.pdf'),
    Literature('IP #12 (The Triangle of Self-Obsession)',
               'https://na.org/wp-content/uploads/2024/05/3112_Triangle-of-Self-Obsession-IP-12-English.pdf'),
    Literature('IP #13 (By Young Addicts)', 'https://na.org/wp-content/uploads/2024/05/EN3113_2008-IP-13-English.pdf'),
    Literature('IP #14 (One Addict\'s Experience)',
                'https://na.org/wp-content/uploads/2024/05/3114_One-Addict-Experience-IP-14-English.pdf'),
     Literature('IP #15 (PI and the NA Member)', 'https://na.org/wp-content/uploads/2024/05/en3115-IP-15-English.pdf'),
     Literature('IP #16 (For the Newcomer)',
                'https://na.org/wp-content/uploads/2024/05/3116_For-Newcomer-IP-16-English.pdf'),
     Literature('IP #17 (For Those in Treatment)',
                'https://na.org/wp-content/uploads/2024/05/EN3117-IP-17-English.pdf'),
     Literature('IP #19 (Self-Acceptance)',
                'https://na.org/wp-content/uploads/2024/05/3119_Self-Acceptance-IP-19-English.pdf'),
     Literature('IP #20 (H&I Service and the NA Member)',
                'https://na.org/wp-content/uploads/2024/05/EN3120-IP-20-English.pdf'),
     Literature('IP #22 (Welcome to NA)', 'https://na.org/wp-content/uploads/2024/05/3122_Welcome-IP-22-English.pdf'),
     Literature('IP #23 (Staying Clean on the Outside)',
                'https://na.org/wp-content/uploads/2024/05/3123_Staying-Clean-IP-23-English.pdf'),
     Literature('IP #24 (Money Matters)', 'https://na.org/wp-content/uploads/2024/05/EN3124-IP-24-English.pdf'),
     Literature('IP #26 (Accessibility)', 'https://na.org/wp-content/uploads/2024/05/EN3126-IP-26-English.pdf'),
     Literature('IP #27 (For the Parents)', 'https://na.org/wp-content/uploads/2024/05/EN3127-IP-27-English.pdf'),
     Literature('IP #28 (Funding NA Services)',
                'https://na.org/wp-content/uploads/2024/05/3128_2024-IP-28-English.pdf'),
     Literature('IP #29 (An Introduction to NA Meetings)',
                'https://na.org/wp-content/uploads/2024/05/EN3129-IP-29-English.pdf'),
     Literature('IP #30 (Mental Health in Recovery)',
                'https://na.org/wp-content/uploads/2024/05/3130_MHR-IP-30-English.pdf'),
     Literature('NA White Booklet', 'https://na.org/wp-content/uploads/2024/05/NA-White-Booklet-English.pdf'),
     Literature('The Group Booklet', 'https://na.org/wp-content/uploads/2024/05/Group-Booklet-English.pdf'),
     Literature('Twelve Concepts for NA Service',
                'https://na.org/wp-content/uploads/2024/05/Twelve-Concepts-English.pdf'),
     Literature('An Introductory Guide to NA',
                'https://na.org/wp-content/uploads/2024/05/1200_Introductory-Guide-English.pdf'),
     Literature('Behind the Walls', 'https://na.org/wp-content/uploads/2024/05/1601_Behind-the-Walls-English.pdf'),
     Literature('In Times of Illness', 'https://na.org/wp-content/uploads/2024/05/In-Times-of-Illness-English.pdf'),
     Literature('Working Step Four in Narcotics Anonymous',
                'https://na.org/wp-content/uploads/2024/05/EN3110-IP-10-English.pdf'),
     Literature('NA: A Resource in Your Community',
                'https://na.org/wp-content/uploads/2024/05/1604_NARS_Aug23-English.pdf'),
     Literature('Guiding Principles: The Spirit of Our Traditions',
                'https://www.na-northernireland.org/wp-content/uploads/2020/04/guiding-principles-sml.pdf'),
     Literature('It Works; How and Why: The Twelve Steps and Twelve Traditions of NA',
                'https://cwpascna.com/wp-content/uploads/2020/06/IT-WORKS-How-and-Why.pdf'),
     Literature('The Narcotics Anonymous Step Working Guide', 'https://gssana.org/books/na-step-working-guide.pdf'),
     Literature('Sponsorship', 'https://www.na-northernireland.org/wp-content/uploads/2020/04/sponsorship.pdf'),
     Literature('Living Clean: The Journey Continues',
                'https://capeatlanticna.org/wp-content/uploads/2013/04/Living-Clean.pdf'),
     Literature('Just for Today: Daily Meditations for Recovering Addicts (JFT)',
                'https://www.nalouisville.net/uploads/4/7/4/3/47431107/justfortoday_med_book.pdf'),
     Literature('A Spiritual Principle a Day (SPAD)',
                'https://www.marscna.org/wp-content/uploads/2022/01/SPAD-ApprovalDraft_Jan22_1_WEB.pdf'),
     Literature('NA Basic Text, Fifth Edition',
                'https://www.nauca.us/wp-content/uploads/2015/05/1988-5th-Edition-Basic-Text-Books-1-2.pdf'),
     Literature('NA Basic Text, Sixth Edition',
                'https://www.nauca.us/wp-content/uploads/2015/05/2008-6th-Edition-NA-Basic-Text.pdf')
     ]

def find_literature_by_keyword(search: str):
    return [
        lit for lit in literature_options if search.lower() in lit.name.lower()
    ]

def find_literature_by_url(url:str):
    for option in literature_options:
        if option.url.lower() == url.lower():
            return option
    return Literature(url, url)