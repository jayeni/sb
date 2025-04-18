from flask import Flask, render_template_string, send_from_directory
from obj_viewer import obj_viewer_bp # Import the Blueprint

app = Flask(__name__, static_folder="assets", static_url_path="/assets")

app.register_blueprint(obj_viewer_bp) # Register the Blueprint

# Add route to serve static files from the main directory
@app.route('/<path:filename>')
def serve_root_files(filename):
    return send_from_directory('.', filename)

@app.route("/")
def mission():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Serene Build</title>
        <!-- Font Awesome for social icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html { 
                height: 100%; /* Ensure html element takes full height */
            }
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
                font-size: 18px;
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
                border: 4px dotted #000080;
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

            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 24px;
                color: #000080;
                margin-top: 10px;
            }

            .projects-grid {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
                gap: 30px;
            }

            .project-card {
                background: #000080;
                border: 2px solid #FFD700;
                border-radius: 10px;
                padding: 20px;
                text-decoration: none;
                transition: transform 0.3s ease;
                display: block;
            }

            .project-card:hover {
                transform: translateY(-5px);
            }

            .project-content {
                text-align: center;
            }

            .project-content h3 {
                color: #FFD700;
                font-family: 'Backso', sans-serif;
                font-size: 24px;
                margin: 0 0 10px 0;
            }

            .project-content p {
                color: white;
                font-family: 'Oswald', sans-serif;
                margin: 0;
            }

            .gallery-container {
                position: relative;
                width: 100%;
                max-width: 1000px;
                margin: 0 auto;
            }
            
            .gallery-slide {
                display: none;
            }
            
            .gallery-slide.active {
                display: block;
            }
            
            .gallery-nav {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin: 20px auto;
                flex-wrap: wrap;
            }
            
            .gallery-button {
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                transition: all 0.3s ease;
                margin: 5px;
            }
            
            .gallery-button:hover {
                background: #FFD700;
                color: #000080;
            }
            
            .gallery-counter {
                font-family: 'Oswald', sans-serif;
                color: #000080;
                font-size: 20px;
                font-weight: bold;
                min-width: 60px;
                text-align: center;
            }

            body {
                font-family: 'Oswald', sans-serif;
                background-color: #ffffff;
                background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('/assets/background-babyblue.png');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed;
                min-height: 100vh;
                margin: 0;
                padding: 0;
                overflow-x: hidden;
            }

            .threejs-container {
                width: 100%;
                max-width: 1200px;
                margin: 30px auto;
                padding: 0;
                background: transparent;
                border-radius: 0;
                box-shadow: none;
                aspect-ratio: 16 / 12;
            }

            #threejs-viewer, #glb-viewer {
                width: 100%;
                max-width: 100%;
                height: 100%;
                display: block;
                margin: 0 auto;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
                overflow: hidden;
            }

            #glb-viewer {
                margin: 0 auto 30px auto;
            }

            .controls {
                margin-top: 25px;
                margin-bottom: 20px;
                text-align: center;
                width: 100%;
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                align-items: center;
                gap: 10px;
            }

            /* Title styling for controls section */
            .controls h4 {
                width: 100%;
                text-align: center;
                font-family: 'Oswald', sans-serif;
                color: #000080;
                margin-bottom: 15px;
                font-size: 22px;
                display: block;
            }

            .controls label, .controls button {
                font-size: 20px;
                margin: 0 5px;
                font-family: 'Oswald', sans-serif;
                font-weight: bold;
                color: #000080;
            }

            .controls input[type="range"] {
                margin: 0 10px;
                transform: scale(1.2);
            }

            .controls input[type="number"], .controls select {
                font-size: 18px;
                padding: 5px;
                margin: 0 5px;
                font-family: 'Oswald', sans-serif;
            }

            .controls input[type="number"]#zoom-input {
                width: 60px;
                text-align: center;
                font-weight: bold;
                background-color: #f0f0f0;
                border: 2px solid #000080;
                border-radius: 4px;
            }

            .controls button {
                padding: 8px 16px;
                font-size: 16px;
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                border-radius: 5px;
                cursor: pointer;
                transition: all 0.3s ease;
                margin: 5px;
            }
            
            .controls button:hover {
                background: #FFD700;
                color: #000080;
                transform: scale(1.05);
            }

            .material-controls {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
                gap: 15px;
                margin-bottom: 15px;
                width: 100%;
            }
            
            .material-control {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 10px;
                background-color: rgba(240, 240, 240, 0.7);
                border: 1px solid #ccc;
                border-radius: 8px;
            }
            
            .material-control:hover {
                box-shadow: 0 0 10px rgba(0, 0, 128, 0.3);
                transform: translateY(-2px);
            }
            
            .material-control label {
                font-size: 16px;
                margin-bottom: 8px;
                font-weight: bold;
                color: #000080;
                text-align: center;
            }
            
            .material-control input[type="color"] {
                width: 80px;
                height: 50px;
                cursor: pointer;
                border: 3px solid #FFD700;
                border-radius: 6px;
                background: none;
                margin-bottom: 12px;
                padding: 2px;
            }
            
            .texture-dropdown {
                margin-top: 5px;
                padding: 5px;
                border: 2px solid #000080;
                border-radius: 4px;
                background-color: white;
                color: #000080;
                font-family: 'Oswald', sans-serif;
                font-size: 14px;
                cursor: pointer;
                width: 120px;
                transition: all 0.2s ease;
            }
            
            .texture-dropdown:hover {
                border-color: #FFD700;
            }

            .coming-soon-text {
                position: relative;
                display: inline-block;
                font-family: 'BubbleStreetFill', sans-serif;
                font-size: 42px;
                color: #228B22;
                margin-left: 20px;
                vertical-align: middle;
                position: relative;
                top: -10px;
            }

            .coming-soon-text::before {
                content: "(Coming Soon)";
                position: absolute;
                left: 0;
                top: 0;
                font-family: 'BubbleStreetOutline', sans-serif;
                color: #000000;
                z-index: 1;
            }

            .coming-soon-text {
                z-index: 2;
            }

            /* Global styles for all color pickers */
            input[type="color"] {
                width: 80px !important;
                height: 50px !important;
                cursor: pointer !important;
                border: 3px solid #FFD700 !important;
                border-radius: 6px !important;
                padding: 2px !important;
                margin: 5px !important;
            }
            
            /* Footer styles */
            .footer {
                background-color: #000080;
                color: white;
                text-align: center;
                padding: 20px 10px;
                margin-top: 60px;
                border-top: 4px solid #FFD700;
                font-family: 'Oswald', sans-serif;
            }
            
            .footer-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .footer-logo {
                font-size: 24px;
                margin-bottom: 15px;
                color: #FFD700;
            }
            
            .footer-links {
                display: flex;
                gap: 30px;
                margin: 15px 0;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .footer-links a {
                color: white;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-links a:hover {
                color: #FFD700;
            }
            
            .footer-social {
                margin: 15px 0;
            }
            
            .footer-social a {
                color: white;
                font-size: 24px;
                margin: 0 10px;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-social a:hover {
                color: #FFD700;
            }
            
            .footer-copyright {
                margin-top: 15px;
                font-size: 14px;
                color: #cccccc;
            }

            .viewer-instructions {
                margin-top: 20px;
                padding: 10px;
                background-color: rgba(240, 240, 240, 0.9);
                border-radius: 8px;
                border: 1px solid #ccc;
                clear: both;
                width: 100%;
            }
            
            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                color: #000080;
                margin: 5px 0;
            }
            
            /* Add responsive styles for smaller screens */
            @media (max-width: 768px) {
                .controls {
                    flex-direction: column;
                    gap: 5px;
                }
                
                .controls button {
                    margin: 3px;
                    font-size: 14px;
                    padding: 6px 10px;
                }
                
                .controls label {
                    font-size: 16px;
                    margin: 3px;
                }
                
                .controls input[type="number"] {
                    width: 50px;
                    font-size: 14px;
                    padding: 3px;
                }
                
                .project-title {
                    font-size: 40px;
                }
                
                .subtitle {
                    font-size: 32px;
                }
                
                .interactive-note {
                    font-size: 16px;
                }
            }

            /* Styles for the link to the separate viewer */
            .viewer-link-card {
                 background: #000080;
                 border: 2px solid #FFD700;
                 border-radius: 10px;
                 padding: 20px;
                 text-decoration: none;
                 transition: transform 0.3s ease;
                 display: block;
                 text-align: center;
                 color: #FFD700; /* Make text gold */
                 font-family: 'Backso', sans-serif;
                 font-size: 24px;
            }
            
            .viewer-link-card:hover {
                 transform: translateY(-5px);
                 background: #FFD700; /* Swap colors on hover */
                 color: #000080;
            }
            
            .viewer-link-card p { /* Style paragraph inside link */
                 color: white;
                 font-family: 'Oswald', sans-serif;
                 margin-top: 10px; /* Add some space */
                 font-size: 16px;
            }
            
            .viewer-link-card:hover p { /* Change paragraph color on hover too */
                 color: #000080;
            }
        </style>
    </head>
    <body>
        <div class="serene-title">
            <span class="combined-bubble-text" data-text="Serene build">Serene build</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js"></script>
        <spline-viewer url="https://prod.spline.design/u2ic6j4HXQpEVlih/scene.splinecode"></spline-viewer>
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all Spline viewers.</div>
        
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

        <div class="subtitle" style="margin-top: 60px;">
            <span class="combined-bubble-text gold" data-text="PROJECTS">PROJECTS</span>
        </div>

        <div class="projects-grid">
            <a href="/projects/adidas-mundial" class="project-card">
                <div class="project-content">
                    <h3>Adidas Mundial Reborn</h3>
                </div>
            </a>
            <a href="/projects/iphone-6" class="project-card">
                <div class="project-content">
                    <h3>Customized Iphone 6</h3>
                </div>
            </a>
            <a href="/projects/repair-estimator" class="project-card">
                <div class="project-content">
                    <h3>Repair Estimator</h3>
                </div>
            </a>
        </div>

        <div class="subtitle" style="margin-top: 60px;">
            <span class="combined-bubble-text gold" data-text="3D MODEL VIEWER - OBJ">3D MODEL VIEWER - OBJ</span>
        </div>

        <!-- Link to the separate OBJ viewer page -->
        <div style="max-width: 1200px; margin: 30px auto; padding: 0 20px;">
             <a href="/obj-viewer" class="viewer-link-card">
                 <div>View Interactive House Model</div>
                 <p>(Click here to open the detailed OBJ model viewer)</p>
            </a>
        </div>
        
        <!-- Removed the OBJ viewer HTML, CSS, and JS from here -->

        <div class="subtitle" style="margin-top: 60px;">
            <span class="combined-bubble-text gold" data-text="3D MODEL VIEWER - GLB(WIP)">3D MODEL VIEWER - GLB(WIP)</span>
        </div>

            <div class="threejs-container">
                <div id="glb-viewer"></div>
        </div>
        
        <div id="object-interaction-area" style="text-align: center; margin-top: 10px; display: flex; justify-content: center; align-items: center; gap: 10px;">
            <span id="clicked-object-display" style="font-family: 'Oswald', sans-serif; color: #000080; font-weight: bold;">
                Clicked: (None)
            </span>
            <input type="color" id="selected-object-color-picker" style="display: none; width: 40px; height: 30px; border: 1px solid #ccc; padding: 2px; cursor: pointer;">
            <button id="toggle-object-visibility" style="display: none; padding: 4px 8px; font-size: 12px;">Hide</button> 
        </div>
        
        <div class="controls">
            <h4>Customize Materials:</h4>
                    <div class="material-controls">
                        <div class="material-control">
                            <label for="glb-shoe-color">Shoe Color:</label>
                            <input type="color" id="glb-shoe-color" value="#FFFFFF">
                        </div>
                    </div>
                    
                    <label for="glb-zoom-input">Zoom:</label>
                    <button id="glb-zoom-out">-</button>
                    <input type="number" id="glb-zoom-input" min="1" max="100" value="25" step="1">
                    <button id="glb-zoom-in">+</button>
                    
                    <button id="glb-rotate-left">Rotate Left</button>
                    <button id="glb-rotate-right">Rotate Right</button>
                    <button id="glb-pause-rotation">Pause</button>
                </div>
        <div class="viewer-instructions">
            <div class="interactive-note">Mouse: Click & drag to rotate. Scroll to zoom. Right-click or Shift + drag to pan.</div>
            <div class="interactive-note">Touch: One finger to rotate. Pinch to zoom. Two fingers to pan.</div>
        </div>

        <style>
            .threejs-container {
                width: 100%;
                max-width: 1200px;
                margin: 30px auto 0 auto; /* Adjust margin */
                padding: 0;
                background: transparent;
                aspect-ratio: 16 / 12; /* Keep aspect ratio for the viewer box */
            }

            #threejs-viewer, #glb-viewer {
                width: 100%;
                height: 100%;
                display: block;
                margin: 0 auto;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
                overflow: hidden;
            }

            #glb-viewer {
                /* No specific margin needed here anymore */
            }

            .controls {
                max-width: 1200px; /* Match container width */
                margin: 20px auto 10px auto; /* Spacing below viewer, above instructions */
                text-align: center;
                width: 95%; /* Slightly less than 100% for padding */
                display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                align-items: center;
                    gap: 10px;
                }
                
            .material-controls {
                display: flex;
                    flex-wrap: wrap;
                    justify-content: center;
                gap: 15px;
                margin-bottom: 15px;
                width: 100%;
            }
            
            .material-control {
                display: flex;
                flex-direction: column;
                align-items: center;
                padding: 10px;
                background-color: rgba(240, 240, 240, 0.7);
                border: 1px solid #ccc;
                border-radius: 8px;
            }

            .viewer-instructions {
                max-width: 1200px; /* Match container width */
                margin: 10px auto 30px auto; /* Spacing below controls */
                    padding: 10px;
                background-color: rgba(240, 240, 240, 0.9);
                border-radius: 8px;
                border: 1px solid #ccc;
                width: 95%; /* Slightly less than 100% for padding */
            }
            
            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                color: #000080;
                margin: 5px 0;
            }
        </style>

        <script type="module">
            import * as THREE from 'https://cdn.skypack.dev/three@0.128.0';
            import { OrbitControls } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/OrbitControls.js';
            import { MTLLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/MTLLoader.js';
            import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/GLTFLoader.js';
            import { EffectComposer } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/EffectComposer.js';
            import { RenderPass } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/RenderPass.js';
            import { OutlinePass } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/OutlinePass.js';

            // Keep GLB viewer variables and functions
            let glbScene, glbCamera, glbRenderer, glbControls, glbCurrentModel; // Added for GLB viewer
            let glbIsRotating = false; // Added for GLB viewer
            let glbRotationDirection = 0; // Added for GLB viewer
            
            // Store references to GLB materials
            let glbMaterials = {
                'shoe': null
            };

            // Removed OBJ specific variables: materials, currentFloorTexture, textureLoader, allLights, initialIntensities, raycaster, mouse, selectedMaterialForEditing, selectedMeshForEditing, composer, outlinePass

            // Removed OBJ init() function

            // Removed OBJ changeMaterialKd() function

            // Removed OBJ setRotation() function

            // Removed OBJ pauseRotation() function

            // Removed OBJ animate() function

            // Removed OBJ loadOBJFile() function

            // Removed OBJ changeZoom() function

            // Removed OBJ zoomIn() function

            // Removed OBJ zoomOut() function

            function initGLBViewer() {
                // Create scene
                glbScene = new THREE.Scene();
                glbScene.background = new THREE.Color(0x000000); // Changed to black background

                // Create camera with matching aspect ratio
                const container = document.getElementById('glb-viewer');
                const aspect = 16 / 12; // Match the container's aspect ratio
                glbCamera = new THREE.PerspectiveCamera(30, aspect, 0.1, 1000);
                // Don't set initial position here, set it after model loads

                // Create renderer with responsive sizing
                glbRenderer = new THREE.WebGLRenderer({ antialias: true });
                glbRenderer.setSize(container.clientWidth, container.clientWidth / aspect);
                glbRenderer.physicallyCorrectLights = true; // Enable physically correct lighting
                glbRenderer.shadowMap.enabled = true; // Enable shadow mapping
                glbRenderer.shadowMap.type = THREE.PCFSoftShadowMap; // Softer shadows
                container.appendChild(glbRenderer.domElement);

                // Add enhanced lighting setup with increased brightness
                const ambientLightGLB = new THREE.AmbientLight(0xffffff, 1.5); // Increased from 0.8 to 1.5
                glbScene.add(ambientLightGLB);
                
                // Main directional light (like sunlight)
                const directionalLightGLB = new THREE.DirectionalLight(0xffffff, 2.5); // Increased from 1.5 to 2.5
                directionalLightGLB.position.set(1, 1, 1);
                directionalLightGLB.castShadow = true;
                glbScene.add(directionalLightGLB);
                
                // Add a second directional light from opposite direction
                const backLightGLB = new THREE.DirectionalLight(0xffffff, 1.5); // Increased from 0.8 to 1.5
                backLightGLB.position.set(-1, 0.5, -1);
                glbScene.add(backLightGLB);
                
                // Add point lights to enhance reflections
                const pointLight1GLB = new THREE.PointLight(0xffffff, 2.0, 50); // Increased from 1.2 to 2.0
                pointLight1GLB.position.set(5, 5, 5);
                glbScene.add(pointLight1GLB);
                
                const pointLight2GLB = new THREE.PointLight(0xffffff, 1.5, 50); // Increased from 1.0 to 1.5
                pointLight2GLB.position.set(-5, 3, -5);
                glbScene.add(pointLight2GLB);
                
                // Add additional point light from below
                const pointLight3GLB = new THREE.PointLight(0xffffff, 1.5, 50);
                pointLight3GLB.position.set(0, -5, 0);
                glbScene.add(pointLight3GLB);

                // Add controls
                glbControls = new OrbitControls(glbCamera, glbRenderer.domElement);
                glbControls.enableDamping = true;
                glbControls.dampingFactor = 0.05;
                glbControls.screenSpacePanning = true;

                // Load GLB file
                loadGLBFile('/assets/currentsneaks.glb');

                // Start animation loop
                animateGLB();

                // Add event listeners for controls
                document.getElementById('glb-zoom-input').addEventListener('input', changeGLBZoom);
                document.getElementById('glb-zoom-in').addEventListener('click', zoomGLBIn);
                document.getElementById('glb-zoom-out').addEventListener('click', zoomGLBOut);
                document.getElementById('glb-rotate-left').addEventListener('click', () => setGLBRotation(-1));
                document.getElementById('glb-rotate-right').addEventListener('click', () => setGLBRotation(1));
                document.getElementById('glb-pause-rotation').addEventListener('click', pauseGLBRotation);
                
                // Add color change listeners for GLB model
                document.getElementById('glb-shoe-color').addEventListener('input', (e) => changeGLBMaterialColor('shoe', e.target.value));
            }

            function animateGLB() {
                requestAnimationFrame(animateGLB);
                if (glbIsRotating && glbCurrentModel) {
                    glbCurrentModel.rotation.y += glbRotationDirection * 0.01;
                }
                glbControls.update();
                glbRenderer.render(glbScene, glbCamera);
            }

            function loadGLBFile(path) {
                const gltfLoader = new GLTFLoader();
                gltfLoader.load(path, function(gltf) {
                    const object = gltf.scene;

                        // Center and scale the model
                        const box = new THREE.Box3().setFromObject(object);
                        const center = box.getCenter(new THREE.Vector3());
                        const size = box.getSize(new THREE.Vector3());

                        const maxDim = Math.max(size.x, size.y, size.z);
                        const scale = 7 / maxDim;
                        object.scale.multiplyScalar(scale);

                        object.position.sub(center.multiplyScalar(scale));

                    // Store references to materials for color changing
                    object.traverse((node) => {
                        if (node.isMesh) {
                            // Assign all meshes to 'shoe' material for uniform coloring
                            if (node.material && node.material.color) {
                                glbMaterials.shoe = node.material;
                            }
                            
                            // Make all materials responsive to lighting
                            if (node.material) {
                                if (Array.isArray(node.material)) {
                                    node.material.forEach(mat => {
                                        mat.metalness = 0.3;
                                        mat.roughness = 0.7;
                                    });
                    } else {
                                    node.material.metalness = 0.3;
                                    node.material.roughness = 0.7;
                                }
                            }
                        }
                    });

                    glbScene.add(object);
                    glbCurrentModel = object;

                    // Set default camera position AFTER model loads
                    glbCamera.position.set(0, 0, 25.0);
                    glbControls.target.set(0, 0, 0);
                    glbControls.update();
                });
            }

            function changeGLBMaterialColor(materialName, colorHex) {
                const material = glbMaterials[materialName];
                if (material) {
                    const color = new THREE.Color(colorHex);
                    
                    // Update the material's color
                    material.color = color;
                    material.needsUpdate = true;
                    console.log(`Changed ${materialName} color to ${colorHex}`);
                            } else {
                    console.warn(`Material '${materialName}' not found for color change`);
                }
            }

            function changeGLBZoom(event) {
                const zoomLevel = parseFloat(event.target.value);
                console.log('GLB zoom level changed to:', zoomLevel);
                glbCamera.position.z = zoomLevel;
                glbControls.update();
            }

            function zoomGLBIn() {
                const input = document.getElementById('glb-zoom-input');
                let currentZoom = parseFloat(input.value);
                let newZoom = Math.max(parseFloat(input.min), currentZoom - 2); // Decrease z for zoom in
                input.value = newZoom;
                glbCamera.position.z = newZoom;
                glbControls.update();
                console.log('GLB Zoom In clicked, new zoom:', newZoom);
            }

            function zoomGLBOut() {
                const input = document.getElementById('glb-zoom-input');
                let currentZoom = parseFloat(input.value);
                let newZoom = Math.min(parseFloat(input.max), currentZoom + 2); // Increase z for zoom out
                input.value = newZoom;
                glbCamera.position.z = newZoom;
                glbControls.update();
                console.log('GLB Zoom Out clicked, new zoom:', newZoom);
            }

            function setGLBRotation(direction) {
                glbRotationDirection = direction;
                glbIsRotating = true;
            }

            function pauseGLBRotation() {
                glbIsRotating = false;
            }

            // Initialize ONLY the GLB viewer when the DOM is loaded
            document.addEventListener('DOMContentLoaded', function() {
            // init(); // Removed OBJ init call
            initGLBViewer(); // Keep GLB init call
                
                // Add window resize event listener for ONLY the GLB viewer
                window.addEventListener('resize', function() {
                    // Removed OBJ viewer resize handling
                    
                    // Handle GLB viewer resize if it exists
                    const glbContainer = document.getElementById('glb-viewer');
                    if (glbContainer && glbRenderer) {
                        const aspect = 16 / 12;
                        if (glbCamera) { // Check if glbCamera is initialized
                            glbCamera.aspect = aspect;
                            glbCamera.updateProjectionMatrix();
                        }
                        glbRenderer.setSize(glbContainer.clientWidth, glbContainer.clientWidth / aspect);
                    }
                });
            });
        </script>

        <div class="footer">
            <div class="footer-content">
                <div class="footer-copyright">SERENE BUILD - IREOLUWA</div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/projects/adidas-mundial")
def adidas_project():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Adidas Mundial Reborn - Serene Build</title>
        <!-- Font Awesome for social icons -->
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <style>
            html { 
                height: 100%; /* Ensure html element takes full height */
            }
            @font-face {
                font-family: 'BubbleStreetFill';
                src: url('/assets/BubbleStreetFill.ttf') format('truetype');
            }

            @font-face {
                font-family: 'BubbleStreetOutline';
                src: url('/assets/BubbleStreetOutline.ttf') format('truetype');
            }
            
            body {
                font-family: 'Oswald', sans-serif;
                /* Faded background: white base + semi-transparent overlay + image */
                background-color: #ffffff; /* Added white background color */
                background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('/assets/background-babyblue.png'); /* Specific property */
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed; /* Re-added fixed attachment */
                min-height: 100vh; /* Ensure body is at least viewport height */
                margin: 0;
                padding: 0;
                overflow-x: hidden; /* Prevent horizontal overflow */
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
                color: #000000;
                z-index: 1;
            }
            
            .combined-bubble-text {
                font-family: 'BubbleStreetFill', sans-serif;
                color: #ec128c;
                z-index: 2;
            }
            
            .combined-bubble-text.gold {
                color: #FFD700;
            }
            
            .project-title {
                font-size: 72px;
                text-align: center;
                margin: 40px 0;
            }

            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 24px;
                color: #000080;
                margin-top: 10px;
            }

            .subtitle {
                font-size: 48px;
                text-align: center;
                margin: 60px 0 20px 0;
            }
            
            .description-text {
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
                text-align: justify;
                font-weight: bold;
                white-space: normal;
                word-spacing: normal;
            }

            .back-button {
                position: fixed;
                top: 20px;
                left: 20px;
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                text-decoration: none;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .back-button:hover {
                background: #FFD700;
                color: #000080;
                transform: translateX(-5px);
            }
            
            /* Footer styles */
            .footer {
                background-color: #000080;
                color: white;
                text-align: center;
                padding: 20px 10px;
                margin-top: 60px;
                border-top: 4px solid #FFD700;
                font-family: 'Oswald', sans-serif;
            }
            
            .footer-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .footer-logo {
                font-size: 24px;
                margin-bottom: 15px;
                color: #FFD700;
            }
            
            .footer-links {
                display: flex;
                gap: 30px;
                margin: 15px 0;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .footer-links a {
                color: white;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-links a:hover {
                color: #FFD700;
            }
            
            .footer-social {
                margin: 15px 0;
            }
            
            .footer-social a {
                color: white;
                font-size: 24px;
                margin: 0 10px;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-social a:hover {
                color: #FFD700;
            }
            
            .footer-copyright {
                margin-top: 15px;
                font-size: 14px;
                color: #cccccc;
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-button">← Back to Home</a>
        
        <div class="project-title">
            <span class="combined-bubble-text" data-text="Adidas Mundial Reborn">Adidas Mundial Reborn</span>
        </div>
        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="CURRENT DESIGN">CURRENT DESIGN</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js"></script>
        <spline-viewer url="https://prod.spline.design/RZQ9qPZ8sRDNd4TP/scene.splinecode"></spline-viewer>
        
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all Spline viewers.</div>
        
        <div class="description-text">
            The adidas Mundial Goal is meant for indoor soccer. It is built for quick cuts, low to the ground control, and a natural feel. The current heel is minimal and low-profile, with just enough padding to keep things snug, but it is not very cushioned. The heel is reinforced for stability, which helps with movement and precision, but you really feel the ground with every step. I have been wearing them for two years, mostly for casual wear and even for skating. I love almost everything about the shoe, especially the fit and the way the upper molds to my foot. But the sole, especially around the heel, is where it does not work for me. It does not give the comfort and support I need for everyday wear, and I do not like the way the heel sole looks. That is the one part I would really want to improve with a new design that is more comfortable.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="DESIGN IDEA 1">DESIGN IDEA 1</span>
        </div>
        
        <div class="gallery-container">
            <div id="viewer-container">
                <!-- Initial viewer will be loaded here -->
            </div>
            
            <div class="gallery-nav">
                <button class="gallery-button" onclick="prevSlide()">Previous</button>
                <span class="gallery-counter">1/3</span>
                <button class="gallery-button" onclick="nextSlide()">Next</button>
            </div>
        </div>

        <script>
            let currentSlide = 1;
            const totalSlides = 3;
            const viewers = [
                'https://prod.spline.design/6ldEPCgiBMqxH8Of/scene.splinecode',
                'https://prod.spline.design/eOY9fdgW-I5bmqYL/scene.splinecode',
                'https://prod.spline.design/fL60YDNXiXb-OYyV/scene.splinecode'
            ];
            
            function loadViewer(index) {
                const container = document.getElementById('viewer-container');
                container.innerHTML = `
                    <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js" defer><\/script>
                    <spline-viewer url="${viewers[index-1]}"></spline-viewer>
                    <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
                    <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all Spline viewers.</div>
                `;
                document.querySelector('.gallery-counter').textContent = `${index}/3`;
            }
            
            function nextSlide() {
                currentSlide = currentSlide >= totalSlides ? 1 : currentSlide + 1;
                loadViewer(currentSlide);
            }
            
            function prevSlide() {
                currentSlide = currentSlide <= 1 ? totalSlides : currentSlide - 1;
                loadViewer(currentSlide);
            }

            // Load the first viewer on page load
            loadViewer(1);
        </script>

        <style>
            .gallery-container {
                position: relative;
                width: 100%;
                max-width: 1000px;
                margin: 0 auto;
            }
            
            #viewer-container spline-viewer {
                width: 100%;
                max-width: 1000px;
                height: 300px;
                display: block;
                margin: 0 auto;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
            }
            
            .gallery-nav {
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 20px;
                margin: 20px auto;
                flex-wrap: wrap;
            }
            
            .gallery-button {
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                transition: all 0.3s ease;
                margin: 5px;
            }
            
            .gallery-button:hover {
                background: #FFD700;
                color: #000080;
            }
            
            .gallery-counter {
                font-family: 'Oswald', sans-serif;
                color: #000080;
                font-size: 20px;
                font-weight: bold;
                min-width: 60px;
                text-align: center;
            }
            
            /* Add responsive styles for smaller screens */
            @media (max-width: 768px) {
                .gallery-container {
                    width: 95%;
                }
                
                #viewer-container spline-viewer {
                    height: 250px;
                }
                
                .gallery-button {
                    padding: 8px 15px;
                    font-size: 16px;
                }
                
                .gallery-counter {
                    font-size: 18px;
                    min-width: 50px;
                }
            }
        </style>

        <div class="description-text">
            One design idea I have is to give the shoe a chunkier sole, similar to what you see on a basketball sneaker. This would add more support and cushioning, making it much more comfortable for casual use. A thicker midsole with better impact protection could help absorb shock during long walks or while skating, and the added height would give the shoe a more modern look. Keeping the upper pattern the same while updating the sole would make it look amazing, combining the classic design with a fresh and functional upgrade.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="DESIGN IDEA 2">DESIGN IDEA 2</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js" defer></script>
        <spline-viewer url="https://prod.spline.design/tSdyENphxBvsK4DK/scene.splinecode"></spline-viewer>
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all viewers.</div>

        <div class="description-text">
            Another idea I have is to make the sneaker completely black. I think an all black colorway would give it a clean and bold look that works well for everyday wear. It would make the shoe easier to style with different outfits and keep it looking fresh even after a lot of use.
        </div>

        <div class="footer">
            <div class="footer-content">
                <div class="footer-copyright">SERENE BUILD - IREOLUWA</div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/projects/iphone-6")
def iphone_project():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Customized Iphone 6 - Serene Build</title>
        <style>
            html { 
                height: 100%; /* Ensure html element takes full height */
            }
            @font-face {
                font-family: 'BubbleStreetFill';
                src: url('/assets/BubbleStreetFill.ttf') format('truetype');
            }

            @font-face {
                font-family: 'BubbleStreetOutline';
                src: url('/assets/BubbleStreetOutline.ttf') format('truetype');
            }
            
            body {
                font-family: 'Oswald', sans-serif;
                /* Faded background: white base + semi-transparent overlay + image */
                background-color: #ffffff; /* Added white background color */
                background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('/assets/background-babyblue.png'); /* Specific property */
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed; /* Re-added fixed attachment */
                min-height: 100vh; /* Ensure body is at least viewport height */
                margin: 0;
                padding: 0;
                overflow-x: hidden; /* Prevent horizontal overflow */
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
                color: #000000;
                z-index: 1;
            }
            
            .combined-bubble-text {
                font-family: 'BubbleStreetFill', sans-serif;
                color: #ec128c;
                z-index: 2;
            }
            
            .combined-bubble-text.gold {
                color: #FFD700;
            }
            
            .project-title {
                font-size: 72px;
                text-align: center;
                margin: 40px 0;
            }

            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 24px;
                color: #000080;
                margin-top: 10px;
            }

            .subtitle {
                font-size: 48px;
                text-align: center;
                margin: 60px 0 20px 0;
            }
            
            .description-text {
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
                text-align: justify;
                font-weight: bold;
                white-space: normal;
                word-spacing: normal;
            }

            .back-button {
                position: fixed;
                top: 20px;
                left: 20px;
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                text-decoration: none;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .back-button:hover {
                background: #FFD700;
                color: #000080;
                transform: translateX(-5px);
            }
            
            /* Footer styles */
            .footer {
                background-color: #000080;
                color: white;
                text-align: center;
                padding: 20px 10px;
                margin-top: 60px;
                border-top: 4px solid #FFD700;
                font-family: 'Oswald', sans-serif;
            }
            
            .footer-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .footer-logo {
                font-size: 24px;
                margin-bottom: 15px;
                color: #FFD700;
            }
            
            .footer-links {
                display: flex;
                gap: 30px;
                margin: 15px 0;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .footer-links a {
                color: white;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-links a:hover {
                color: #FFD700;
            }
            
            .footer-social {
                margin: 15px 0;
            }
            
            .footer-social a {
                color: white;
                font-size: 24px;
                margin: 0 10px;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-social a:hover {
                color: #FFD700;
            }
            
            .footer-copyright {
                margin-top: 15px;
                font-size: 14px;
                color: #cccccc;
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-button">← Back to Home</a>
        
        <div class="project-title">
            <span class="combined-bubble-text" data-text="Customized Iphone 6">Customized Iphone 6</span>
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="CURRENT DESIGN">CURRENT DESIGN</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js" defer></script>
        <spline-viewer url="https://prod.spline.design/w72fhOcXgE578Oby/scene.splinecode"></spline-viewer>
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all Spline viewers.</div>
        
        <div class="description-text">
            The iPhone 6 was my favorite phone of all time. It had such a sleek, clean design that just felt right in the hand. What really made it stand out was that it was the last iPhone to support using wired headphones through the headphone jack while charging at the same time, without needing any adapters or workarounds. It was simple, functional, and smooth, everything a phone should be.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="DESIGN IDEA 1">DESIGN IDEA 1</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js" defer></script>
        <spline-viewer url="https://prod.spline.design/lBFbuSgCCapAM3gp/scene.splinecode"></spline-viewer>
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all Spline viewers.</div>

        <div class="description-text">
            I want to redesign the iPhone 6 in matte black to give it a more modern, stealthy look. The original finishes were nice, but a matte black version would make it feel fresh and timeless. I'm planning to either wrap it with a clean vinyl skin or swap out the housing entirely to get that smooth, soft matte texture that doesn't catch too much light.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="DESIGN IDEA 2">DESIGN IDEA 2</span>
        </div>

        <div class="description-text">
            For my second design idea, I want to load the iPhone 6 with custom apps tailored for sports lovers and financial literacy. These are apps I plan to build myself, inspired by my passion for sharing knowledge and my love for data science. The goal is to create tools that are both useful and personal, apps that help people track stats, stay motivated, and learn how to better manage their money, all from a device that feels like a custom built experience.
        </div>

        <div class="footer">
            <div class="footer-content">
                <div class="footer-copyright">SERENE BUILD - IREOLUWA</div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

@app.route("/projects/repair-estimator")
def repair_estimator_project():
    html = '''
    <!DOCTYPE html>
    <html>
    <head>
        <title>Repair Estimator - Serene Build</title>
        <style>
            html { 
                height: 100%; /* Ensure html element takes full height */
            }
            @font-face {
                font-family: 'BubbleStreetFill';
                src: url('/assets/BubbleStreetFill.ttf') format('truetype');
            }

            @font-face {
                font-family: 'BubbleStreetOutline';
                src: url('/assets/BubbleStreetOutline.ttf') format('truetype');
            }
            
            body {
                font-family: 'Oswald', sans-serif;
                /* Faded background: white base + semi-transparent overlay + image */
                background-color: #ffffff; /* Added white background color */
                background-image: linear-gradient(rgba(255, 255, 255, 0.75), rgba(255, 255, 255, 0.75)), url('/assets/background-babyblue.png'); /* Specific property */
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                background-attachment: fixed; /* Added fixed background attachment like iPhone page */
                min-height: 100vh; /* Ensure body is at least viewport height */
                margin: 0;
                padding: 0;
                overflow-x: hidden; /* Prevent horizontal overflow like iPhone page */
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
                color: #000000;
                z-index: 1;
            }
            
            .combined-bubble-text {
                font-family: 'BubbleStreetFill', sans-serif;
                color: #ec128c;
                z-index: 2;
            }
            
            .combined-bubble-text.gold {
                color: #FFD700;
            }
            
            .project-title {
                font-size: 72px;
                text-align: center;
                margin: 40px 0;
            }

            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 24px;
                color: #000080;
                margin-top: 10px;
            }

            .subtitle {
                font-size: 48px;
                text-align: center;
                margin: 60px 0 20px 0;
            }
            
            .description-text {
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                line-height: 1.6;
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
                text-align: justify;
                font-weight: bold;
                white-space: normal;
                word-spacing: normal;
            }

            .back-button {
                position: fixed;
                top: 20px;
                left: 20px;
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                font-size: 18px;
                text-decoration: none;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .back-button:hover {
                background: #FFD700;
                color: #000080;
                transform: translateX(-5px);
            }

            .coming-soon-text {
                position: relative;
                display: inline-block;
                font-family: 'BubbleStreetFill', sans-serif;
                font-size: 42px;
                color: #228B22;
                margin-left: 20px;
                vertical-align: middle;
                position: relative;
                top: -10px;
            }

            .coming-soon-text::before {
                content: "(Coming Soon)";
                position: absolute;
                left: 0;
                top: 0;
                font-family: 'BubbleStreetOutline', sans-serif;
                color: #000000;
                z-index: 1;
            }

            .coming-soon-text {
                z-index: 2;
            }
            
            .viewer-link-card {
                 background: #000080;
                 border: 2px solid #FFD700;
                 border-radius: 10px;
                 padding: 20px;
                 text-decoration: none;
                 transition: transform 0.3s ease;
                 display: block;
                 text-align: center;
                 color: #FFD700; /* Make text gold */
                 font-family: 'Backso', sans-serif;
                 font-size: 24px;
            }
            
            .viewer-link-card:hover {
                 transform: translateY(-5px);
                 background: #FFD700; /* Swap colors on hover */
                 color: #000080;
            }
            
            .viewer-link-card p { /* Style paragraph inside link */
                 color: white;
                 font-family: 'Oswald', sans-serif;
                 margin-top: 10px; /* Add some space */
                 font-size: 16px;
            }
            
            .viewer-link-card:hover p { /* Change paragraph color on hover too */
                 color: #000080;
            }

            /* Footer styles - Copied from main page */
            .footer {
                background-color: #000080;
                color: white;
                text-align: center;
                padding: 20px 10px;
                margin-top: 60px;
                border-top: 4px solid #FFD700;
                font-family: 'Oswald', sans-serif;
            }
            
            .footer-content {
                display: flex;
                flex-direction: column;
                align-items: center;
                max-width: 1200px;
                margin: 0 auto;
            }
            
            .footer-logo {
                font-size: 24px;
                margin-bottom: 15px;
                color: #FFD700;
            }
            
            .footer-links {
                display: flex;
                gap: 30px;
                margin: 15px 0;
                flex-wrap: wrap;
                justify-content: center;
            }
            
            .footer-links a {
                color: white;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-links a:hover {
                color: #FFD700;
            }
            
            .footer-social {
                margin: 15px 0;
            }
            
            .footer-social a {
                color: white;
                font-size: 24px;
                margin: 0 10px;
                text-decoration: none;
                transition: color 0.3s ease;
            }
            
            .footer-social a:hover {
                color: #FFD700;
            }
            
            .footer-copyright {
                margin-top: 15px;
                font-size: 14px;
                color: #cccccc;
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-button">← Back to Home</a>
        
        <div class="project-title">
            <span class="combined-bubble-text" data-text="Repair Estimator">Repair Estimator</span>
            <span class="coming-soon-text">(Coming Soon)</span>
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="QUICK & ACCURATE RENOVATION COST ESTIMATES">QUICK & ACCURATE RENOVATION COST ESTIMATES</span>
        </div>
        
        <div class="description-text">
            Repair Estimator is a tool that shows a 3D model of different rooms in a house. Users can look at each room by itself or view the whole house together. In each room, users can change the type of floor by picking from a list that includes hardwood, tile, carpet, and more. Each flooring option shows how much it costs, so users can see how their choices affect the total price.
            <br><br>
            Users can also change the color of the walls using different paint options. Each paint color will have a cost, which helps users plan their budget. In the future, the tool may also let users add furniture to the rooms. Each piece of furniture will have a price too. This will help users see what their space could look like when it's fully set up, with all costs included.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="3D MODEL VIEWER - OBJ">3D MODEL VIEWER - OBJ</span>
        </div>

        <!-- Link to the separate OBJ viewer page -->
        <div style="max-width: 1200px; margin: 30px auto; padding: 0 20px;">
             <a href="/obj-viewer" class="viewer-link-card">
                 <div>View Interactive House Model</div>
                 <p>(Click here to open the detailed OBJ model viewer)</p>
            </a>
        </div>

        <div class="footer">
            <div class="footer-content">
                <div class="footer-copyright">SERENE BUILD - IREOLUWA</div>
            </div>
        </div>
    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)