import pyfiglet

def draw_welcome_AI_BITS():
    # Create an instance of the Figlet class
    font = pyfiglet.Figlet()

    # Generate ASCII art for the text "Ironman"
    ascii_art = font.renderText("WELCOME TO"+"\n"+"AI - BITS : )")
    
    # Print the ASCII art
    print(ascii_art)
   
    print("""
    El desarrollo de este lenguaje fue durante el primer Hackathon de Código Facilito.
    Antes no habíamos pensado en desarrollar un proyecto de este calibre pero este hackathon
    nos ha animado a ver el límite de nuestras capacidades en pro del conocimiento. El proceso
    ha sido retador, interesante y satisfactorio. Se decidió usar el nombre de  AI-Bits por la
    combinación de inteligencia artificial y bits, la unidad mínima de información. Es así como
    nace AI-Bits, un lenguaje que integra sintaxis de programación e inteligencia artificial y se
    enfoca a la educación y al aprendizaje.
    """+"\n")
    