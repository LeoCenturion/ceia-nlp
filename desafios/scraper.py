import os
import re
import time
import requests
from bs4 import BeautifulSoup

books_to_download = [
    # Volume 4
    {"author": "Homer", "title": "The Iliad"},
    {"author": "Homer", "title": "The Odyssey"},
    # Volume 5
    {"author": "Aeschylus", "title": "The Suppliant Maidens"},
    {"author": "Aeschylus", "title": "The Persians"},
    {"author": "Aeschylus", "title": "Seven Against Thebes"},
    {"author": "Aeschylus", "title": "Prometheus Bound"},
    {"author": "Aeschylus", "title": "Agamemnon"},
    {"author": "Aeschylus", "title": "Choephoroe"},
    {"author": "Aeschylus", "title": "The Eumenides"},
    {"author": "Sophocles", "title": "Oedipus the King"},
    {"author": "Sophocles", "title": "Oedipus at Colonus"},
    {"author": "Sophocles", "title": "Antigone"},
    {"author": "Sophocles", "title": "Ajax"},
    {"author": "Sophocles", "title": "Electra"},
    {"author": "Sophocles", "title": "The Trachiniae"},
    {"author": "Sophocles", "title": "Philoctetes"},
    {"author": "Euripides", "title": "Rhesus"},
    {"author": "Euripides", "title": "Medea"},
    {"author": "Euripides", "title": "Hippolytus"},
    {"author": "Euripides", "title": "Alcestis"},
    {"author": "Euripides", "title": "Heracleidae"},
    {"author": "Euripides", "title": "The Suppliants"},
    {"author": "Euripides", "title": "The Trojan Women"},
    {"author": "Euripides", "title": "Ion"},
    {"author": "Euripides", "title": "Helen"},
    {"author": "Euripides", "title": "Andromache"},
    {"author": "Euripides", "title": "Electra"}, # Euripides' Electra
    {"author": "Euripides", "title": "Bacchantes"},
    {"author": "Euripides", "title": "Hecuba"},
    {"author": "Euripides", "title": "Heracles Mad"},
    {"author": "Euripides", "title": "The Phoenician Women"},
    {"author": "Euripides", "title": "Orestes"},
    {"author": "Euripides", "title": "Iphigenia in Tauris"},
    {"author": "Euripides", "title": "Iphigenia in Aulis"},
    {"author": "Euripides", "title": "Cyclops"},
    {"author": "Aristophanes", "title": "The Acharnians"},
    {"author": "Aristophanes", "title": "The Knights"},
    {"author": "Aristophanes", "title": "The Clouds"},
    {"author": "Aristophanes", "title": "The Wasps"},
    {"author": "Aristophanes", "title": "Peace"},
    {"author": "Aristophanes", "title": "The Birds"},
    {"author": "Aristophanes", "title": "The Frogs"},
    {"author": "Aristophanes", "title": "Lysistrata"},
    {"author": "Aristophanes", "title": "Thesmophoriazusae"},
    {"author": "Aristophanes", "title": "Ecclesiazousae"},
    {"author": "Aristophanes", "title": "Plutus"},
    # Volume 6
    {"author": "Herodotus", "title": "The History"},
    {"author": "Thucydides", "title": "History of the Peloponnesian War"},
    # Volume 7
    {"author": "Plato", "title": "Charmides"},
    {"author": "Plato", "title": "Lysis"},
    {"author": "Plato", "title": "Laches"},
    {"author": "Plato", "title": "Protagoras"},
    {"author": "Plato", "title": "Euthydemus"},
    {"author": "Plato", "title": "Cratylus"},
    {"author": "Plato", "title": "Phaedrus"},
    {"author": "Plato", "title": "Ion"}, # Plato's Ion
    {"author": "Plato", "title": "Symposium"},
    {"author": "Plato", "title": "Meno"},
    {"author": "Plato", "title": "Euthyphro"},
    {"author": "Plato", "title": "Apology"},
    {"author": "Plato", "title": "Crito"},
    {"author": "Plato", "title": "Phaedo"},
    {"author": "Plato", "title": "Gorgias"},
    {"author": "Plato", "title": "The Republic"},
    {"author": "Plato", "title": "Timaeus"},
    {"author": "Plato", "title": "Critias"},
    {"author": "Plato", "title": "Parmenides"},
    {"author": "Plato", "title": "Theaetetus"},
    {"author": "Plato", "title": "Sophist"},
    {"author": "Plato", "title": "Statesman"},
    {"author": "Plato", "title": "Philebus"},
    {"author": "Plato", "title": "Laws"},
    {"author": "Plato", "title": "The Seventh Letter"},
    # Volume 8
    {"author": "Aristotle", "title": "Categories"},
    {"author": "Aristotle", "title": "On Interpretation"},
    {"author": "Aristotle", "title": "Prior Analytics"},
    {"author": "Aristotle", "title": "Posterior Analytics"},
    {"author": "Aristotle", "title": "Topics"},
    {"author": "Aristotle", "title": "Sophistical Refutations"},
    {"author": "Aristotle", "title": "Physics"},
    {"author": "Aristotle", "title": "On the Heavens"},
    {"author": "Aristotle", "title": "On Generation and Corruption"},
    {"author": "Aristotle", "title": "Meteorology"},
    {"author": "Aristotle", "title": "Metaphysics"},
    {"author": "Aristotle", "title": "On the Soul"},
    {"author": "Aristotle", "title": "On Sense and the Sensible"},
    {"author": "Aristotle", "title": "On Memory and Reminisence"},
    {"author": "Aristotle", "title": "On Sleep and Sleeplessness"},
    {"author": "Aristotle", "title": "On Dreams"},
    {"author": "Aristotle", "title": "On Prophesying by Dreams"},
    {"author": "Aristotle", "title": "On Longevity and Shortness of Life"},
    {"author": "Aristotle", "title": "On Youth and Old Age, On Life and Death, On Breathing"},
    # Volume 9
    {"author": "Aristotle", "title": "History of Animals"},
    {"author": "Aristotle", "title": "Parts of Animals"},
    {"author": "Aristotle", "title": "On the Motion of Animals"},
    {"author": "Aristotle", "title": "On the Gait of Animals"},
    {"author": "Aristotle", "title": "On the Generation of Animals"},
    {"author": "Aristotle", "title": "Nicomachean Ethics"},
    {"author": "Aristotle", "title": "Politics"},
    {"author": "Aristotle", "title": "The Athenian Constitution"},
    {"author": "Aristotle", "title": "Rhetoric"},
    {"author": "Aristotle", "title": "Poetics"},
    # Volume 10
    {"author": "Hippocrates", "title": "The Hippocratic Oath"},
    {"author": "Hippocrates", "title": "On Ancient Medicine"},
    {"author": "Hippocrates", "title": "On Airs, Water, and Places"},
    {"author": "Hippocrates", "title": "The Book of Prognostics"},
    {"author": "Hippocrates", "title": "On Regimen in Acute Diseases"},
    {"author": "Hippocrates", "title": "Of the Epidemics"},
    {"author": "Hippocrates", "title": "On Injuries of the Head"},
    {"author": "Hippocrates", "title": "On the Surgery"},
    {"author": "Hippocrates", "title": "On Fractures"},
    {"author": "Hippocrates", "title": "On the Articulations"},
    {"author": "Hippocrates", "title": "Instruments of Reduction"},
    {"author": "Hippocrates", "title": "Aphorisms"},
    {"author": "Hippocrates", "title": "The Law"},
    {"author": "Hippocrates", "title": "The Ulcer"},
    {"author": "Hippocrates", "title": "On Fistulae"},
    {"author": "Hippocrates", "title": "On Hemorrhoids"},
    {"author": "Hippocrates", "title": "On the Sacred Disease"},
    {"author": "Galen", "title": "On the Natural Faculties"},
    # Volume 11
    {"author": "Euclid", "title": "The Thirteen Books of Euclid's Elements"},
    {"author": "Archimedes", "title": "On the Sphere and Cylinder"},
    {"author": "Archimedes", "title": "Measurement of a Circle"},
    {"author": "Archimedes", "title": "On Conoids and Spheroids"},
    {"author": "Archimedes", "title": "On Spirals"},
    {"author": "Archimedes", "title": "On the Equilibrium of Planes"},
    {"author": "Archimedes", "title": "The Sand Reckoner"},
    {"author": "Archimedes", "title": "The Quadrature of the Parabola"},
    {"author": "Archimedes", "title": "On Floating Bodies"},
    {"author": "Archimedes", "title": "Book of Lemmas"},
    {"author": "Archimedes", "title": "The Method Treating of Mechanical Problems"},
    {"author": "Apollonius of Perga", "title": "On Conic Sections"},
    {"author": "Nicomachus of Gerasa", "title": "Introduction to Arithmetic"},
    # Volume 12
    {"author": "Lucretius", "title": "On the Nature of Things"},
    {"author": "Epictetus", "title": "The Discourses"},
    {"author": "Marcus Aurelius", "title": "The Meditations"},
    # Volume 13
    {"author": "Virgil", "title": "Eclogues"},
    {"author": "Virgil", "title": "Georgics"},
    {"author": "Virgil", "title": "Aeneid"},
    # Volume 14
    {"author": "Plutarch", "title": "The Lives of the Noble Grecians and Romans"},
    # Volume 15
    {"author": "P. Cornelius Tacitus", "title": "The Annals"},
    {"author": "P. Cornelius Tacitus", "title": "The Histories"},
    # Volume 16
    {"author": "Ptolemy", "title": "Almagest"},
    {"author": "Nicolaus Copernicus", "title": "On the Revolutions of Heavenly Spheres"},
    {"author": "Johannes Kepler", "title": "Epitome of Copernican Astronomy (Books IV–V)"},
    {"author": "Johannes Kepler", "title": "The Harmonies of the World (Book V)"},
    # Volume 17
    {"author": "Plotinus", "title": "The Six Enneads"},
    # Volume 18
    {"author": "Augustine of Hippo", "title": "The Confessions"},
    {"author": "Augustine of Hippo", "title": "The City of God"},
    {"author": "Augustine of Hippo", "title": "On Christian Doctrine"},
    # Volume 19 & 20
    {"author": "Thomas Aquinas", "title": "Summa Theologica"}, # Single entry for Summa Theologica
    # Volume 21
    {"author": "Dante Alighieri", "title": "Divine Comedy"},
    # Volume 22
    {"author": "Geoffrey Chaucer", "title": "Troilus and Criseyde"},
    {"author": "Geoffrey Chaucer", "title": "The Canterbury Tales"},
    # Volume 23
    {"author": "Niccolò Machiavelli", "title": "The Prince"},
    {"author": "Thomas Hobbes", "title": "Leviathan"},
    # Volume 24
    {"author": "François Rabelais", "title": "Gargantua and Pantagruel"},
    # Volume 25
    {"author": "Michel Eyquem de Montaigne", "title": "Essays"},
    # Volume 26 (William Shakespeare)
    {"author": "William Shakespeare", "title": "The First Part of King Henry the Sixth"},
    {"author": "William Shakespeare", "title": "The Second Part of King Henry the Sixth"},
    {"author": "William Shakespeare", "title": "The Third Part of King Henry the Sixth"},
    {"author": "William Shakespeare", "title": "The Tragedy of Richard the Third"},
    {"author": "William Shakespeare", "title": "The Comedy of Errors"},
    {"author": "William Shakespeare", "title": "Titus Andronicus"},
    {"author": "William Shakespeare", "title": "The Taming of the Shrew"},
    {"author": "William Shakespeare", "title": "The Two Gentlemen of Verona"},
    {"author": "William Shakespeare", "title": "Love's Labour's Lost"},
    {"author": "William Shakespeare", "title": "Romeo and Juliet"},
    {"author": "William Shakespeare", "title": "The Tragedy of King Richard the Second"},
    {"author": "William Shakespeare", "title": "A Midsummer Night's Dream"},
    {"author": "William Shakespeare", "title": "The Life and Death of King John"},
    {"author": "William Shakespeare", "title": "The Merchant of Venice"},
    {"author": "William Shakespeare", "title": "The First Part of King Henry the Fourth"},
    {"author": "William Shakespeare", "title": "The Second Part of King Henry the Fourth"},
    {"author": "William Shakespeare", "title": "Much Ado About Nothing"},
    {"author": "William Shakespeare", "title": "The Life of King Henry the Fifth"},
    {"author": "William Shakespeare", "title": "Julius Caesar"},
    {"author": "William Shakespeare", "title": "As You Like It"},
    # Volume 27 (William Shakespeare)
    {"author": "William Shakespeare", "title": "Twelfth Night; or, What You Will"},
    {"author": "William Shakespeare", "title": "The Tragedy of Hamlet, Prince of Denmark"},
    {"author": "William Shakespeare", "title": "The Merry Wives of Windsor"},
    {"author": "William Shakespeare", "title": "Troilus and Cressida"},
    {"author": "William Shakespeare", "title": "All's Well That Ends Well"},
    {"author": "William Shakespeare", "title": "Measure for Measure"},
    {"author": "William Shakespeare", "title": "Othello, the Moor of Venice"},
    {"author": "William Shakespeare", "title": "King Lear"},
    {"author": "William Shakespeare", "title": "Macbeth"},
    {"author": "William Shakespeare", "title": "Antony and Cleopatra"},
    {"author": "William Shakespeare", "title": "Coriolanus"},
    {"author": "William Shakespeare", "title": "Timon of Athens"},
    {"author": "William Shakespeare", "title": "Pericles, Prince of Tyre"},
    {"author": "William Shakespeare", "title": "Cymbeline"},
    {"author": "William Shakespeare", "title": "The Winter's Tale"},
    {"author": "William Shakespeare", "title": "The Tempest"},
    {"author": "William Shakespeare", "title": "The Famous History of the Life of King Henry the Eighth"},
    {"author": "William Shakespeare", "title": "Sonnets"},
    # Volume 28
    {"author": "William Gilbert", "title": "On the Loadstone and Magnetic Bodies"},
    {"author": "Galileo Galilei", "title": "Dialogues Concerning the Two New Sciences"},
    {"author": "William Harvey", "title": "On the Motion of the Heart and Blood in Animals"},
    {"author": "William Harvey", "title": "On the Circulation of Blood"},
    {"author": "William Harvey", "title": "On the Generation of Animals"},
    # Volume 29
    {"author": "Miguel de Cervantes", "title": "The History of Don Quixote de la Mancha"},
    # Volume 30
    {"author": "Sir Francis Bacon", "title": "The Advancement of Learning"},
    {"author": "Sir Francis Bacon", "title": "Novum Organum"},
    {"author": "Sir Francis Bacon", "title": "New Atlantis"},
    # Volume 31
    {"author": "René Descartes", "title": "Rules for the Direction of the Mind"},
    {"author": "René Descartes", "title": "Discourse on the Method"},
    {"author": "René Descartes", "title": "Meditations on First Philosophy"},
    {"author": "René Descartes", "title": "Objections Against the Meditations and Replies"},
    {"author": "René Descartes", "title": "The Geometry"},
    {"author": "Benedict de Spinoza", "title": "Ethics"},
    # Volume 32 (John Milton)
    {"author": "John Milton", "title": "On the Morning of Christ's Nativity"},
    {"author": "John Milton", "title": "A Paraphrase on Psalm 114"},
    {"author": "John Milton", "title": "Psalm 136"},
    {"author": "John Milton", "title": "The Passion"},
    {"author": "John Milton", "title": "On Time"},
    {"author": "John Milton", "title": "Upon the Circumcision"},
    {"author": "John Milton", "title": "At a Solemn Musick"},
    {"author": "John Milton", "title": "An Epitaph on the Marchioness of Winchester"},
    {"author": "John Milton", "title": "Song on May Morning"},
    {"author": "John Milton", "title": "On Shakespeare"},
    {"author": "John Milton", "title": "On the University Carrier"},
    {"author": "John Milton", "title": "Another on the same"}, # This title might be hard to find
    {"author": "John Milton", "title": "L'Allegro"},
    {"author": "John Milton", "title": "Il Penseroso"},
    {"author": "John Milton", "title": "Arcades"},
    {"author": "John Milton", "title": "Lycida"},
    {"author": "John Milton", "title": "Comus"},
    {"author": "John Milton", "title": "On the Death of a Fair Infant"},
    {"author": "John Milton", "title": "At a Vacation Exercise"},
    {"author": "John Milton", "title": "The Fifth Ode of Horace"},
    {"author": "John Milton", "title": "Sonnets"}, # General collection of his sonnets
    {"author": "John Milton", "title": "On the New Forcers of Conscience"},
    {"author": "John Milton", "title": "On the Lord General Fairfax at the Siege of Colchester"},
    {"author": "John Milton", "title": "To the Lord General Cromwell"},
    {"author": "John Milton", "title": "To Sir Henry Vane the Younger"},
    {"author": "John Milton", "title": "To Mister Cyriack the Skinner upon his Blindness"},
    {"author": "John Milton", "title": "Selected Psalms"}, # Representing Psalms (I—VIII & LXXX—LXXXVIII)
    {"author": "John Milton", "title": "Paradise Lost"},
    {"author": "John Milton", "title": "Samson Agonistes"},
    {"author": "John Milton", "title": "Areopagitica"},
    # Volume 33
    {"author": "Blaise Pascal", "title": "The Provincial Letters"},
    {"author": "Blaise Pascal", "title": "Pensées"},
    {"author": "Blaise Pascal", "title": "Scientific and mathematical essays"}, # Generic, may not be a single book
    # Volume 34
    {"author": "Sir Isaac Newton", "title": "Mathematical Principles of Natural Philosophy"},
    {"author": "Sir Isaac Newton", "title": "Optics"},
    {"author": "Christiaan Huygens", "title": "Treatise on Light"},
    # Volume 35
    {"author": "John Locke", "title": "A Letter Concerning Toleration"},
    {"author": "John Locke", "title": "Concerning Civil Government, Second Essay"},
    {"author": "John Locke", "title": "An Essay Concerning Human Understanding"},
    {"author": "George Berkeley", "title": "The Principles of Human Knowledge"},
    {"author": "David Hume", "title": "An Enquiry Concerning Human Understanding"},
    # Volume 36
    {"author": "Jonathan Swift", "title": "Gulliver's Travels"},
    {"author": "Laurence Sterne", "title": "The Life and Opinions of Tristram Shandy, Gentleman"},
    # Volume 37
    {"author": "Henry Fielding", "title": "The History of Tom Jones, a Foundling"},
    # Volume 38
    {"author": "Charles de Secondat, Baron de Montesquieu", "title": "The Spirit of the Laws"},
    {"author": "Jean Jacques Rousseau", "title": "A Discourse on the Origin of Inequality"},
    {"author": "Jean Jacques Rousseau", "title": "A Discourse on Political Economy"},
    {"author": "Jean Jacques Rousseau", "title": "The Social Contract"},
    # Volume 39
    {"author": "Adam Smith", "title": "An Inquiry into the Nature and Causes of the Wealth of Nations"},
    # Volume 40 & 41
    {"author": "Edward Gibbon", "title": "The Decline and Fall of the Roman Empire"}, # Single entry
    # Volume 42 (Immanuel Kant)
    {"author": "Immanuel Kant", "title": "Critique of Pure Reason"},
    {"author": "Immanuel Kant", "title": "Fundamental Principles of the Metaphysic of Morals"},
    {"author": "Immanuel Kant", "title": "Critique of Practical Reason"},
    {"author": "Immanuel Kant", "title": "Preface and Introduction to the Metaphysical Elements of Ethics with a note on Conscience"},
    {"author": "Immanuel Kant", "title": "General Introduction to the Metaphysic of Morals"},
    {"author": "Immanuel Kant", "title": "The Science of Right"},
    {"author": "Immanuel Kant", "title": "The Critique of Judgement"},
    # Volume 43
    {"author": "American State Papers", "title": "Declaration of Independence"}, # Or Thomas Jefferson / Continental Congress
    {"author": "American State Papers", "title": "Articles of Confederation"}, # Or Continental Congress
    {"author": "American State Papers", "title": "The Constitution of the United States of America"}, # Or Constitutional Convention
    {"author": "Alexander Hamilton, James Madison, John Jay", "title": "The Federalist"},
    {"author": "John Stuart Mill", "title": "On Liberty"},
    {"author": "John Stuart Mill", "title": "Considerations on Representative Government"},
    {"author": "John Stuart Mill", "title": "Utilitarianism"},
    # Volume 44
    {"author": "James Boswell", "title": "The Life of Samuel Johnson, LL.D."},
    # Volume 45
    {"author": "Antoine Laurent Lavoisier", "title": "Elements of Chemistry"},
    {"author": "Jean Baptiste Joseph Fourier", "title": "Analytical Theory of Heat"},
    {"author": "Michael Faraday", "title": "Experimental Researches in Electricity"},
    # Volume 46
    {"author": "Georg Wilhelm Friedrich Hegel", "title": "The Philosophy of Right"},
    {"author": "Georg Wilhelm Friedrich Hegel", "title": "The Philosophy of History"},
    # Volume 47
    {"author": "Johann Wolfgang von Goethe", "title": "Faust"},
    # Volume 48
    {"author": "Herman Melville", "title": "Moby Dick; or, The Whale"},
    # Volume 49
    {"author": "Charles Darwin", "title": "The Origin of Species by Means of Natural Selection"},
    {"author": "Charles Darwin", "title": "The Descent of Man, and Selection in Relation to Sex"},
    # Volume 50
    {"author": "Karl Marx", "title": "Capital"},
    {"author": "Karl Marx and Friedrich Engels", "title": "Manifesto of the Communist Party"},
    # Volume 51
    {"author": "Count Leo Tolstoy", "title": "War and Peace"},
    # Volume 52
    {"author": "Fyodor Mikhailovich Dostoevsky", "title": "The Brothers Karamazov"},
    # Volume 53
    {"author": "William James", "title": "The Principles of Psychology"},
    # Volume 54 (Sigmund Freud)
    {"author": "Sigmund Freud", "title": "The Origin and Development of Psycho-Analysis"},
    {"author": "Sigmund Freud", "title": "Selected Papers on Hysteria"},
    {"author": "Sigmund Freud", "title": "The Sexual Enlightenment of Children"},
    {"author": "Sigmund Freud", "title": "The Future Prospects of Psycho-Analytic Therapy"},
    {"author": "Sigmund Freud", "title": "Observations on \"Wild\" Psycho-Analysis"},
    {"author": "Sigmund Freud", "title": "The Interpretation of Dreams"},
    {"author": "Sigmund Freud", "title": "On Narcissism"},
    {"author": "Sigmund Freud", "title": "Instincts and Their Vicissitudes"},
    {"author": "Sigmund Freud", "title": "Repression"},
    {"author": "Sigmund Freud", "title": "The Unconscious"},
    {"author": "Sigmund Freud", "title": "A General Introduction to Psycho-Analysis"},
    {"author": "Sigmund Freud", "title": "Beyond the Pleasure Principle"},
    {"author": "Sigmund Freud", "title": "Group Psychology and the Analysis of the Ego"},
    {"author": "Sigmund Freud", "title": "The Ego and the Id"},
    {"author": "Sigmund Freud", "title": "Inhibitions, Symptoms, and Anxiety"},
    {"author": "Sigmund Freud", "title": "Thoughts for the Times on War and Death"},
    {"author": "Sigmund Freud", "title": "Civilization and Its Discontents"},
    {"author": "Sigmund Freud", "title": "New Introductory Lectures on Psycho-Analysis"},
]

# Directory to save downloaded books
DOWNLOAD_DIR = "gutenberg_ebooks"

# User-Agent to identify your script
USER_AGENT = "GutenbergBookDownloader/1.0 (Python Script; +http://your-contact-info-if-any.com)"

# Delay between requests to be polite to the server (in seconds)
REQUEST_DELAY = 2

# --- Helper Functions ---

def sanitize_filename(author, title):
    """Creates a safe filename from author and title."""
    filename = f"{author} - {title}.txt"
    # Remove characters that are invalid in filenames
    filename = re.sub(r'[<>:"/\\|?*]', '_', filename)
    # Replace multiple spaces/underscores with a single underscore
    filename = re.sub(r'\s+', '_', filename)
    filename = re.sub(r'_+', '_', filename)
    # Limit length to avoid issues with long filenames
    return filename[:240] # Max filename length can be an issue

def make_absolute_url(base_url, link):
    """Converts a relative URL to an absolute URL."""
    if link.startswith("//"):
        return "https:" + link
    if link.startswith("/"):
        return base_url.rstrip('/') + link
    if not link.startswith(("http://", "https://")):
        return base_url.rstrip('/') + '/' + link.lstrip('/')
    return link

# --- Main Script ---

def download_books():
    """
    Iterates through the book list, searches for them on Project Gutenberg,
    and attempts to download the plain text UTF-8 versions.
    """
    if not os.path.exists(DOWNLOAD_DIR):
        print(f"Creating directory: {DOWNLOAD_DIR}")
        os.makedirs(DOWNLOAD_DIR)

    for book_info in books_to_download:
        author = book_info["author"]
        title = book_info["title"]
        
        print(f"\nProcessing: {title} by {author}")
        
        sanitized_file_name = sanitize_filename(author, title)
        file_path = os.path.join(DOWNLOAD_DIR, sanitized_file_name)

        if os.path.exists(file_path):
            print(f"Skipping '{sanitized_file_name}', already downloaded.")
            continue

        try:
            # 1. Search for the book
            search_query = f"{title} {author}"
            search_url = f"https://www.gutenberg.org/ebooks/search/?query={requests.utils.quote(search_query)}"
            
            print(f"Searching at: {search_url}")
            search_response = requests.get(search_url, headers={"User-Agent": USER_AGENT}, timeout=30)
            search_response.raise_for_status() # Raise an exception for HTTP errors
            time.sleep(REQUEST_DELAY)

            search_soup = BeautifulSoup(search_response.content, 'html.parser')
            
            # Find the first book link in the search results
            book_link_tag = search_soup.find('li', class_='booklink')
            if not book_link_tag or not book_link_tag.find('a'):
                print(f"Could not find a direct book link for '{title} by {author}' in search results.")
                continue
            
            ebook_page_relative_url = book_link_tag.find('a')['href']
            ebook_page_url = make_absolute_url("https://www.gutenberg.org", ebook_page_relative_url)
            
            print(f"Found ebook page: {ebook_page_url}")

            # 2. Go to the ebook page and find the plain text download link
            ebook_response = requests.get(ebook_page_url, headers={"User-Agent": USER_AGENT}, timeout=30)
            ebook_response.raise_for_status()
            time.sleep(REQUEST_DELAY)
            
            ebook_soup = BeautifulSoup(ebook_response.content, 'html.parser')
            
            # Try to find the "Plain Text UTF-8" link
            # Common patterns for plain text links:
            # - type="text/plain; charset=utf-8"
            # - text containing "Plain Text UTF-8"
            # - href ending in .txt, -0.txt, or -8.txt
            
            download_link_tag = ebook_soup.find('a', type='text/plain; charset=utf-8')
            
            if not download_link_tag: # Fallback: search for link text
                download_link_tag = ebook_soup.find('a', string=re.compile(r'Plain Text UTF-8', re.IGNORECASE))

            if not download_link_tag: # Fallback: search for .txt in href
                txt_links = ebook_soup.find_all('a', href=re.compile(r'\.txt$|-0\.txt$|-8\.txt$', re.IGNORECASE))
                if txt_links:
                    # Prefer links with 'files' in them and containing the ebook ID from the page URL
                    ebook_id_match = re.search(r'/ebooks/(\d+)', ebook_page_url)
                    if ebook_id_match:
                        ebook_id = ebook_id_match.group(1)
                        for link_tag in txt_links:
                            if f"/files/{ebook_id}/" in link_tag['href']:
                                download_link_tag = link_tag
                                break
                    if not download_link_tag and txt_links: # if specific one not found, take the first generic .txt
                         download_link_tag = txt_links[0]


            if not download_link_tag or not download_link_tag.has_attr('href'):
                print(f"Could not find a plain text download link for '{title} by {author}' on page {ebook_page_url}")
                continue

            text_file_relative_url = download_link_tag['href']
            text_file_url = make_absolute_url("https://www.gutenberg.org", text_file_relative_url)
            
            print(f"Found text download link: {text_file_url}")

            # 3. Download the text file
            text_response = requests.get(text_file_url, headers={"User-Agent": USER_AGENT}, timeout=60)
            text_response.raise_for_status()
            text_response.encoding = 'utf-8' # Ensure correct encoding

            # 4. Save the book
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text_response.text)
            print(f"Successfully downloaded and saved: {sanitized_file_name}")

        except requests.exceptions.RequestException as e:
            print(f"Error downloading '{title} by {author}': {e}")
        except AttributeError as e:
            print(f"Error parsing page for '{title} by {author}' (likely unexpected HTML structure): {e}")
        except Exception as e:
            print(f"An unexpected error occurred for '{title} by {author}': {e}")
        
        finally:
            # Ensure there's a delay even if an error occurs before the next attempt
            time.sleep(REQUEST_DELAY / 2) # Shorter delay if an error occurred on this book

    print("\nFinished downloading all specified books.")

if __name__ == "__main__":
    # Before running, make sure you have populated the 'books_to_download' list.
    if not books_to_download or (len(books_to_download) == 1 and books_to_download[0]['title'] == "Example Book"):
        print("Please edit the script and populate the 'books_to_download' list before running.")
    else:
        download_books()
