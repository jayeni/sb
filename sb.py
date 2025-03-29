from flask import Flask, render_template_string

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

@app.route("/")
def mission():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Serene Build</title>
        <style>
            @font-face {
                font-family: 'BubbleStreetFill';
                src: url('/assets/BubbleStreetFill.ttf') format('truetype');
            }

            @font-face {
                font-family: 'BubbleStreetOutline';
                src: url('/assets/BubbleStreetOutline.ttf') format('truetype');
            }

            @font-face {
                font-family: 'Expressionista';
                src: url('/assets/ExpressionistaDemo-6R47A.ttf') format('truetype');
            }

            @font-face {
                font-family: 'Oswald';
                src: url('/assets/Oswald-Regular.ttf') format('truetype');
            }

            @font-face {
                font-family: 'Backso';
                src: url('/assets/Backso.ttf') format('truetype');
            }
            
            spline-viewer {
                width: 1000px;
                height: 300px;
                display: block;
                margin: 0 auto;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
            }
            
            .custom-text {
                font-family: 'MonkBones', sans-serif;
                font-size: 48px;
                text-align: center;
                margin: 20px 0;
                color: #000080;
            }

            .mission-text {
                font-family: 'Backso', sans-serif;
                font-size: 36px;
                text-align: center;
                margin: 20px 20px;
                color: #FFD700;
            }

            .description-text {
                font-family: 'Oswald', sans-serif;
                font-size: 16px;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
                text-align: justify;
                font-weight: bold;
                white-space: normal;
                word-spacing: normal;
            }

            .quote {
                font-style: italic;
                margin-top: 20px;
                text-align: center;
            }

            .timeline {
                width: 1000px;
                height: 1000px;
                margin: 40px auto;
                position: relative;
            }

            /* Circle background */
            .circle-background {
                position: absolute;
                width: 600px;
                height: 600px;
                border: 4px dotted #FFD700;
                border-radius: 50%;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                z-index: 0;
            }

            .timeline-item {
                position: absolute;
                width: 200px;
                padding: 20px;
                background: #fff;
                border: 2px solid #000080;
                border-radius: 8px;
                text-align: center;
                z-index: 1;
            }

            .timeline-number {
                position: absolute;
                top: -15px;
                left: -15px;
                width: 30px;
                height: 30px;
                background-color: #000080;
                color: white;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-family: 'Oswald', sans-serif;
                font-weight: bold;
                font-size: 18px;
            }

            .timeline-title {
                font-family: 'Oswald', sans-serif;
                color: #000080;
                font-size: 18px;
                margin-bottom: 10px;
                text-align: center;
            }

            .timeline-content {
                font-family: 'Oswald', sans-serif;
                font-size: 14px;
                line-height: 1.4;
                text-align: center;
            }

            /* Position boxes around the circle */
            .timeline-item:nth-child(2) { top: 100px; left: 400px; } /* Top (1) */
            .timeline-item:nth-child(3) { top: 200px; left: 100px; } /* Top Left (2) - was position 6 */
            .timeline-item:nth-child(4) { top: 500px; left: 100px; } /* Bottom Left (3) - was position 5 */
            .timeline-item:nth-child(5) { top: 700px; left: 400px; } /* Bottom (4) */
            .timeline-item:nth-child(6) { top: 500px; left: 700px; } /* Bottom Right (5) */
            .timeline-item:nth-child(7) { top: 200px; left: 700px; } /* Top Right (6) */

            .process-title {
                font-family: 'Backso', sans-serif;
                font-size: 48px;
                text-align: center;
                color: #FFD700;
                margin-bottom: 60px;
            }

            .combined-bubble-text {
                position: relative;
                display: inline-block;
            }
            
            .combined-bubble-text::before {
                content: attr(data-text);
                position: absolute;
                left: 0;
                top: 0;
                font-family: 'BubbleStreetOutline', sans-serif;
                color: #000000;  /* Default black outline */
                z-index: 1;
            }
            
            .combined-bubble-text {
                font-family: 'BubbleStreetFill', sans-serif;
                color: #ec128c;  /* Original pink color */
                z-index: 2;
            }
            
            .combined-bubble-text.gold {
                color: #FFD700;  /* Gold fill for subtitles (changed from navy) */
            }
            
            .serene-title {
                font-size: 94px;
                text-align: center;
                margin: 20px 0;
            }
            
            .subtitle {
                font-size: 48px;
                text-align: center;
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="serene-title">
            <span class="combined-bubble-text" data-text="Serene build">Serene build</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js"></script>
        <spline-viewer url="https://prod.spline.design/u2ic6j4HXQpEVlih/scene.splinecode"></spline-viewer>
        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="JOURNEY">JOURNEY</span>
        </div>
        
        <div class="description-text">
            I have been at peace solving challenging problems. I have always had a creative passion for renewing and repairing things, whether it was a broken chair, broken phone, broken laptop, faulty door and a lot of other entities that I use on a daily basis. I consider myself a student of knowledge and books are one way to stay a student. I'm always on the hunt for books that help me discover who I am through questioning what I already know. I never found myself familiar with public libraries because the books were never my cup of tea. I always found the books I wanted on abebooks or in a private library not near me. I never had a space in my parents house to collect books and films to collect to share with others. I now have grown to accept a mission to build my own library for books, films, electronics, furniture and art that give me knowledge of Life. I have acquired a property based on this mission. But at the core idea is to renew and continue to work on the foundation of what we know, by this I mean repairing and renewing what already exists in this world.
            
            <div class="quote">
                "Any sufficiently advanced skill looks like a superpower until you learn it, and then it becomes just another tool in your toolbox."
            </div>
            
            <div style="padding:52.42% 0 0 0;position:relative;"><iframe src="https://player.vimeo.com/video/1070450398?h=9fe4dd58b6&amp;title=0&amp;byline=0&amp;portrait=0&amp;badge=0&amp;autopause=0&amp;player_id=0&amp;app_id=58479" frameborder="0" allow="autoplay; fullscreen; picture-in-picture; clipboard-write; encrypted-media" style="position:absolute;top:0;left:0;width:100%;height:100%;" title="sb"></iframe></div><script src="https://player.vimeo.com/api/player.js"></script>
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="CREATIVE PROCESS">CREATIVE PROCESS</span>
        </div>
        
        <div class="timeline">
            <div class="circle-background"></div>
            
            <div class="timeline-item">
                <div class="timeline-number">1</div>
                <div class="timeline-title">Seek Entity requiring restoration</div>
                <div class="timeline-content">
                    Initial assessment and identification of items needing restoration work.
                </div>
            </div>

            <div class="timeline-item">
                <div class="timeline-number">2</div>
                <div class="timeline-title">3D model Entity requiring restoration</div>
                <div class="timeline-content">
                    Creating detailed 3D models of the item to document current condition using CAD software.
                </div>
            </div>

            <div class="timeline-item">
                <div class="timeline-number">3</div>
                <div class="timeline-title">3D model possible restoration outcomes</div>
                <div class="timeline-content">
                    Visualizing different restoration approaches and their potential results using CAD software.
                </div>
            </div>

            <div class="timeline-item">
                <div class="timeline-number">4</div>
                <div class="timeline-title">Price restoration</div>
                <div class="timeline-content">
                    Evaluating costs and providing estimates for the restoration work.
                </div>
            </div>

            <div class="timeline-item">
                <div class="timeline-number">5</div>
                <div class="timeline-title">Restore Entity</div>
                <div class="timeline-content">
                    Executing the restoration work according to the chosen approach.
                </div>
            </div>

            <div class="timeline-item">
                <div class="timeline-number">6</div>
                <div class="timeline-title">Document Restoration</div>
                <div class="timeline-content">
                    Capture photos, videos, and written records of the restoration process to track progress and ensure transparency.
                </div>
            </div>
        </div>

    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)