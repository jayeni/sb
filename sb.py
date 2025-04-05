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

            .interactive-note {
                text-align: center;
                font-family: 'Oswald', sans-serif;
                font-size: 16px;
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
                width: 1000px;
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
            }
            
            .gallery-button {
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                transition: all 0.3s ease;
            }
            
            .gallery-button:hover {
                background: #FFD700;
                color: #000080;
            }
            
            .gallery-counter {
                font-family: 'Oswald', sans-serif;
                color: #000080;
                font-size: 18px;
                font-weight: bold;
                min-width: 60px;
                text-align: center;
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
        </div>

        <div class="subtitle" style="margin-top: 60px;">
            <span class="combined-bubble-text gold" data-text="3D MODEL VIEWER - OBJ(WIP)">3D MODEL VIEWER - OBJ(WIP)</span>
        </div>

        <div class="threejs-container">
            <div id="threejs-viewer"></div>
            <div class="controls">
                <label for="color-picker">Change Color:</label>
                <input type="color" id="color-picker" value="#00ff00">
                <input type="text" id="hex-input" placeholder="#00ff00" value="#00ff00" maxlength="7">
                
                <label for="zoom-input">Zoom:</label>
                <button id="zoom-out">-</button>
                <input type="number" id="zoom-input" min="1" max="100" value="20" step="1">
                <button id="zoom-in">+</button>
                
                <button id="rotate-left">Rotate Left</button>
                <button id="rotate-right">Rotate Right</button>
                <button id="pause-rotation">Pause</button>
            </div>
        </div>

        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all viewers.</div>

        <div class="subtitle" style="margin-top: 60px;">
            <span class="combined-bubble-text gold" data-text="3D MODEL VIEWER - GLB(WIP)">3D MODEL VIEWER - GLB(WIP)</span>
        </div>

        <div class="threejs-container">
            <div id="glb-viewer"></div>
            <div class="controls">
                <label for="glb-color-picker">Change Color:</label>
                <input type="color" id="glb-color-picker" value="#00ff00">
                <input type="text" id="glb-hex-input" placeholder="#00ff00" value="#00ff00" maxlength="7">
                
                <label for="glb-zoom-input">Zoom:</label>
                <button id="glb-zoom-out">-</button>
                <input type="number" id="glb-zoom-input" min="1" max="100" value="25" step="1">
                <button id="glb-zoom-in">+</button>
                
                <button id="glb-rotate-left">Rotate Left</button>
                <button id="glb-rotate-right">Rotate Right</button>
                <button id="glb-pause-rotation">Pause</button>
            </div>
        </div>

        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all viewers.</div>

        <script type="module">
            import * as THREE from 'https://cdn.skypack.dev/three@0.128.0';
            import { OrbitControls } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/OrbitControls.js';
            import { OBJLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/OBJLoader.js';
            import { GLTFLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/GLTFLoader.js';

            let scene, camera, renderer, controls, currentModel;
            let isRotating = false;
            let rotationDirection = 0;

            let glbScene, glbCamera, glbRenderer, glbControls, glbCurrentModel;
            let glbIsRotating = false;
            let glbRotationDirection = 0;

            function init() {
                // Create scene
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0xffffff);

                // Create camera
                camera = new THREE.PerspectiveCamera(30, 1000 / 600, 0.1, 1000);

                // Create renderer
                renderer = new THREE.WebGLRenderer({ antialias: true });
                renderer.setSize(1000, 600);
                document.getElementById('threejs-viewer').appendChild(renderer.domElement);

                // Add lights
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
                scene.add(ambientLight);
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(1, 1, 1);
                scene.add(directionalLight);

                // Add controls
                controls = new OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.screenSpacePanning = true;

                // Load OBJ file
                loadOBJFile('/assets/parkwood3.obj');

                // Start animation loop
                animate();

                // Add event listeners for controls
                document.getElementById('color-picker').addEventListener('input', changeColor);
                document.getElementById('zoom-input').addEventListener('input', changeZoom);
                document.getElementById('zoom-in').addEventListener('click', zoomIn);
                document.getElementById('zoom-out').addEventListener('click', zoomOut);
                document.getElementById('rotate-left').addEventListener('click', () => setRotation(-1));
                document.getElementById('rotate-right').addEventListener('click', () => setRotation(1));
                document.getElementById('pause-rotation').addEventListener('click', pauseRotation);
                document.getElementById('hex-input').addEventListener('input', changeColorFromHex);
            }

            function setRotation(direction) {
                rotationDirection = direction;
                isRotating = true;
            }

            function pauseRotation() {
                isRotating = false;
            }

            function animate() {
                requestAnimationFrame(animate);
                if (isRotating && currentModel) {
                    currentModel.rotation.y += rotationDirection * 0.01; // Continuous rotation based on direction
                }
                controls.update();
                renderer.render(scene, camera);
            }

            function loadOBJFile(path) {
                const objLoader = new OBJLoader();
                objLoader.load(path, function(object) {
                    // Center and scale the model
                    const box = new THREE.Box3().setFromObject(object);
                    const center = box.getCenter(new THREE.Vector3());
                    const size = box.getSize(new THREE.Vector3());

                    const maxDim = Math.max(size.x, size.y, size.z);
                    const scale = 7 / maxDim;
                    object.scale.multiplyScalar(scale);

                    object.position.sub(center.multiplyScalar(scale));

                    scene.add(object);
                    currentModel = object;

                    // Reset camera position
                    camera.position.set(0, 0, 20.0);
                    controls.target.set(0, 0, 0);
                    controls.update();

                    // Set default color to green by forcing a basic green material
                    const greenMaterial = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
                    object.traverse((child) => {
                        if (child.isMesh) {
                            child.material = greenMaterial;
                        }
                    });
                });
            }

            function updateHexInput(color) {
                document.getElementById('hex-input').value = `#${color.getHexString()}`;
            }

            function changeColor(event) {
                const color = new THREE.Color(event.target.value);
                if (currentModel) {
                    currentModel.traverse((child) => {
                        if (child.isMesh) {
                            child.material.color.set(color);
                        }
                    });
                }
                updateHexInput(color);
            }

            function changeZoom(event) {
                const zoomLevel = parseFloat(event.target.value);
                console.log('Zoom level changed via slider to:', zoomLevel);
                camera.position.z = zoomLevel;
                controls.update();
            }

            function zoomIn() {
                const slider = document.getElementById('zoom-input');
                let currentZoom = parseFloat(slider.value);
                let newZoom = Math.max(parseFloat(slider.min), currentZoom - 2); // Decrease z for zoom in
                slider.value = newZoom;
                camera.position.z = newZoom;
                controls.update();
                console.log('Zoom In clicked, new zoom:', newZoom);
            }

            function zoomOut() {
                const slider = document.getElementById('zoom-input');
                let currentZoom = parseFloat(slider.value);
                let newZoom = Math.min(parseFloat(slider.max), currentZoom + 2); // Increase z for zoom out
                slider.value = newZoom;
                camera.position.z = newZoom;
                controls.update();
                console.log('Zoom Out clicked, new zoom:', newZoom);
            }

            function changeColorFromHex(event) {
                const hexValue = event.target.value;
                if (/^#[0-9A-Fa-f]{6}$/.test(hexValue)) {
                    const color = new THREE.Color(hexValue);
                    if (currentModel) {
                        currentModel.traverse((child) => {
                            if (child.isMesh) {
                                child.material.color.set(color);
                            }
                        });
                    }
                    updateHexInput(color);
                }
            }

            function initGLBViewer() {
                // Create scene
                glbScene = new THREE.Scene();
                glbScene.background = new THREE.Color(0xffffff);

                // Create camera
                glbCamera = new THREE.PerspectiveCamera(30, 1200 / 800, 0.1, 1000);
                // Don't set initial position here, set it after model loads

                // Create renderer
                glbRenderer = new THREE.WebGLRenderer({ antialias: true });
                glbRenderer.setSize(1200, 800);
                document.getElementById('glb-viewer').appendChild(glbRenderer.domElement);

                // Add lights
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.5);
                glbScene.add(ambientLight);
                const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8);
                directionalLight.position.set(1, 1, 1);
                glbScene.add(directionalLight);

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
                document.getElementById('glb-color-picker').addEventListener('input', changeGLBColor);
                document.getElementById('glb-hex-input').addEventListener('input', changeGLBColorFromHex);
                document.getElementById('glb-zoom-input').addEventListener('input', changeGLBZoom);
                document.getElementById('glb-zoom-in').addEventListener('click', zoomGLBIn);
                document.getElementById('glb-zoom-out').addEventListener('click', zoomGLBOut);
                document.getElementById('glb-rotate-left').addEventListener('click', () => setGLBRotation(-1));
                document.getElementById('glb-rotate-right').addEventListener('click', () => setGLBRotation(1));
                document.getElementById('glb-pause-rotation').addEventListener('click', pauseGLBRotation);
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

                    glbScene.add(object);
                    glbCurrentModel = object;

                    // Set default camera position AFTER model loads
                    glbCamera.position.set(0, 0, 25.0);
                    glbControls.target.set(0, 0, 0);
                    glbControls.update();

                    // Set default color to green
                    object.traverse((child) => {
                        if (child.isMesh) {
                            child.material.color.set('#00ff00');
                        }
                    });
                });
            }

            function changeGLBColor(event) {
                const color = new THREE.Color(event.target.value);
                if (glbCurrentModel) {
                    glbCurrentModel.traverse((child) => {
                        if (child.isMesh) {
                            child.material.color.set(color);
                        }
                    });
                }
                updateGLBHexInput(color);
            }

            function changeGLBColorFromHex(event) {
                const hexValue = event.target.value;
                if (/^#[0-9A-Fa-f]{6}$/.test(hexValue)) {
                    const color = new THREE.Color(hexValue);
                    if (glbCurrentModel) {
                        glbCurrentModel.traverse((child) => {
                            if (child.isMesh) {
                                child.material.color.set(color);
                            }
                        });
                    }
                    updateGLBHexInput(color);
                }
            }

            function updateGLBHexInput(color) {
                document.getElementById('glb-hex-input').value = `#${color.getHexString()}`;
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

            // Initialize viewer
            init();
            initGLBViewer();
        </script>

        <style>
            .threejs-container {
                width: 1000px;
                margin: 40px auto;
                padding: 20px;
                background: #f5f5f5;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(0, 0, 0, 0.1);
            }

            #threejs-viewer {
                width: 1000px;
                height: 600px;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
                overflow: hidden;
            }

            .controls {
                margin-top: 20px;
                text-align: center;
            }

            .controls label, .controls button {
                font-size: 24px;
                margin: 0 10px;
                font-family: 'Oswald', sans-serif;
                font-weight: bold;
            }

            .controls input[type="color"], .controls input[type="range"] {
                margin: 0 10px;
                transform: scale(1.2);
            }

            .controls input[type="text"], .controls input[type="number"], .controls select {
                font-size: 20px;
                padding: 5px;
                margin: 0 10px;
                font-family: 'Oswald', sans-serif;
            }

            .controls input[type="number"]#zoom-input {
                width: 70px;
                text-align: center;
                font-weight: bold;
                background-color: #f0f0f0;
                border: 2px solid #000080;
                border-radius: 4px;
            }

            .controls button {
                padding: 8px 16px;
                font-size: 22px;
            }

            #glb-viewer {
                width: 1000px;
                height: 600px;
                border: 4px solid #FFD700;
                border-radius: 10px;
                box-shadow: 0 0 15px rgba(255, 215, 0, 0.4);
                outline: 4px solid #ec128c;
                overflow: hidden;
                margin: 20px auto;
                display: block;
            }
        </style>

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
        <style>
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
                font-size: 16px;
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
                text-decoration: none;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .back-button:hover {
                background: #FFD700;
                color: #000080;
                transform: translateX(-5px);
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
                width: 1000px;
                margin: 0 auto;
            }
            
            #viewer-container spline-viewer {
                width: 1000px;
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
            }
            
            .gallery-button {
                background: #000080;
                color: #FFD700;
                border: 2px solid #FFD700;
                padding: 10px 20px;
                border-radius: 5px;
                cursor: pointer;
                font-family: 'Oswald', sans-serif;
                transition: all 0.3s ease;
            }
            
            .gallery-button:hover {
                background: #FFD700;
                color: #000080;
            }
            
            .gallery-counter {
                font-family: 'Oswald', sans-serif;
                color: #000080;
                font-size: 18px;
                font-weight: bold;
                min-width: 60px;
                text-align: center;
            }
        </style>

        <div class="description-text">
            One design idea I have is to give the shoe a chunkier sole, similar to what you see on a basketball sneaker. This would add more support and cushioning, making it much more comfortable for casual use. A thicker midsole with better impact protection could help absorb shock during long walks or while skating, and the added height would give the shoe a more modern look. Keeping the upper pattern the same while updating the sole would make it look amazing, combining the classic design with a fresh and functional upgrade.
        </div>

        <div class="subtitle">
            <span class="combined-bubble-text gold" data-text="DESIGN IDEA 2">DESIGN IDEA 2</span>
        </div>
        
        <script type="module" src="https://unpkg.com/@splinetool/viewer@1.9.82/build/spline-viewer.js"></script>
        <spline-viewer url="https://prod.spline.design/tSdyENphxBvsK4DK/scene.splinecode"></spline-viewer>
        <div class="interactive-note">This viewer is interactive. Click and drag to explore!</div>
        <div class="interactive-note">Use two fingers on mobile to interact with 3D objects in all viewers.</div>

        <div class="description-text">
            Another idea I have is to make the sneaker completely black. I think an all black colorway would give it a clean and bold look that works well for everyday wear. It would make the shoe easier to style with different outfits and keep it looking fresh even after a lot of use.
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
                font-size: 16px;
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
                text-decoration: none;
                transition: all 0.3s ease;
                z-index: 1000;
            }
            
            .back-button:hover {
                background: #FFD700;
                color: #000080;
                transform: translateX(-5px);
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

    </body>
    </html>
    '''
    return render_template_string(html)

if __name__ == '__main__':
    app.run(debug=True)