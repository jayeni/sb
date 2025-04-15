from flask import Blueprint, render_template_string

# Create a Blueprint
obj_viewer_bp = Blueprint('obj_viewer', __name__, url_prefix='/obj-viewer')

@obj_viewer_bp.route('/')
def show_obj_viewer():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>OBJ Model Viewer - Serene Build</title>
        <style>
            /* Base styles from sb.py (body, fonts, etc.) */
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
                font-family: 'Oswald';
                src: url('/assets/Oswald-Regular.ttf') format('truetype');
            }
            
            @font-face {
                 font-family: 'Backso';
                 src: url('/assets/Backso.ttf') format('truetype');
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

            /* Styles for combined bubble text (copied from sb.py) */
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
            
            .viewer-title { /* Using a specific class for the title on this page */
                font-size: 72px;
                text-align: center;
                margin: 40px 0;
            }
            
            .subtitle {
                 font-size: 48px;
                 text-align: center;
                 margin: 60px 0 20px 0;
             }

            /* Back button style (copied from project pages) */
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

            /* OBJ viewer specific styles (copied from sb.py) */
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

            #threejs-viewer { /* Target the specific viewer ID */
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
                position: relative; /* Needed for absolute positioning of the menu */
            }
            
             /* Model Groups Menu Styling (copied from sb.py) */
            #model-groups-menu {
                position: absolute;
                left: 0;
                top: 0;
                width: 250px;
                height: 100%;
                background-color: rgba(30, 30, 30, 0.9);
                color: white;
                padding: 10px;
                overflow-y: auto;
                transition: transform 0.3s ease;
                z-index: 1000;
                box-shadow: 2px 0px 5px rgba(0, 0, 0, 0.5);
                box-sizing: border-box; /* Include padding in width/height */
            }

            #model-groups-menu h3 {
                margin: 0 0 15px 0; /* Adjusted margin */
                font-size: 16px;
            }
            
            .model-group-item {
                margin-bottom: 10px;
                padding: 8px;
                border-radius: 4px;
                background-color: rgba(60, 60, 60, 0.7);
                transition: background-color 0.2s ease; /* Smooth background transition */
            }
            
            .model-group-item:hover {
                 background-color: rgba(75, 75, 75, 0.8); /* Slightly lighter on hover */
             }
            
            .model-group-header { /* Changed class name for clarity */
                display: flex;
                align-items: center;
                margin-bottom: 8px;
                cursor: pointer;
                user-select: none;
                padding: 4px; /* Add padding for easier clicking */
                 border-radius: 3px; /* Rounded corners for the header area */
            }
            
             .model-group-header:hover {
                 background-color: rgba(90, 90, 90, 0.5); /* Highlight header on hover */
             }
             
            .model-group-icon { /* Changed class name */
                margin-right: 8px;
                font-size: 12px;
                color: rgba(180, 180, 180, 1);
                line-height: 1; /* Ensure icon aligns well */
            }
            
            .model-group-name { /* Changed class name */
                font-size: 13px;
                font-weight: bold;
                overflow: hidden;
                text-overflow: ellipsis;
                white-space: nowrap;
                flex-grow: 1; /* Allow name to take available space */
            }
            
             /* Controls within the group item */
             .model-group-controls { /* Changed class name */
                 display: flex;
                 flex-direction: column;
                 gap: 8px;
                 margin-top: 5px; /* Add space below header */
             }
             
             .model-group-controls input[type="color"],
             .model-group-controls select,
             .model-group-controls button {
                 width: 100%;
                 padding: 4px; /* Smaller padding */
                 margin: 0; /* Remove default margins */
                 font-size: 12px; /* Smaller font size */
                 background-color: #555;
                 color: white;
                 border: 1px solid #777; /* Slightly lighter border */
                 border-radius: 3px;
                 cursor: pointer;
                 box-sizing: border-box; /* Ensure padding doesn't increase size */
             }
             
             .model-group-controls input[type="color"] {
                 height: 30px; /* Adjust height for color picker */
                 padding: 2px; /* Minimal padding */
             }
             
             .model-group-controls label {
                 display: block;
                 margin-bottom: 3px;
                 font-size: 12px;
                 color: rgba(200, 200, 200, 1);
             }
             
             .model-group-controls button:hover {
                 background-color: #666;
             }
             
              /* Menu Header specific styles */
             #model-menu-header { /* Specific ID for header */
                 display: flex;
                 justify-content: space-between;
                 align-items: center;
                 margin-bottom: 15px;
             }
             
             #model-menu-collapse-btn { /* Specific ID for button */
                 background: none;
                 border: 1px solid white;
                 color: white;
                 width: 24px;
                 height: 24px;
                 cursor: pointer;
                 display: flex;
                 justify-content: center;
                 align-items: center;
                 border-radius: 3px;
                 font-size: 16px; /* Make symbols clearer */
                 line-height: 1;
             }
            
            /* Copied controls styling from sb.py */
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
             
             .control-section { /* Added for grouping */
                 width: 100%;
                 margin-bottom: 20px;
                 padding: 15px;
                 background-color: rgba(240, 240, 240, 0.7);
                 border-radius: 8px;
                 border: 1px solid #ccc;
             }

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
                 vertical-align: middle; /* Align range slider better */
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
                 transition: all 0.2s ease; /* Add transition */
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
                 width: 80px !important; /* Use important to override potential conflicts */
                 height: 50px !important;
                 cursor: pointer !important;
                 border: 3px solid #FFD700 !important;
                 border-radius: 6px !important;
                 background: none; /* Ensure picker style is clean */
                 margin-bottom: 12px !important;
                 padding: 2px !important;
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

             /* Camera and Environment Controls Grouping */
             .camera-controls, .environment-controls {
                  display: flex;
                  flex-wrap: wrap;
                  justify-content: center;
                  align-items: center;
                  gap: 10px;
             }
             
             .environment-controls input[type="color"] {
                 width: 50px !important; /* Smaller color picker for background */
                 height: 30px !important;
                 cursor: pointer !important;
                 border: 3px solid #FFD700 !important;
                 border-radius: 4px !important;
                 padding: 1px !important;
                 vertical-align: middle;
             }
             
             /* Object Interaction Area Styling */
            #object-interaction-area {
                text-align: center;
                margin-top: 15px; /* Increased margin */
                margin-bottom: 15px; /* Added bottom margin */
                display: flex;
                justify-content: center;
                align-items: center;
                gap: 15px; /* Increased gap */
                padding: 10px;
                background-color: rgba(240, 240, 240, 0.8); /* Light background */
                border-radius: 8px;
                max-width: 600px; /* Limit width */
                margin-left: auto;
                margin-right: auto;
             }

             #clicked-object-display {
                 font-family: 'Oswald', sans-serif;
                 color: #000080;
                 font-weight: bold;
                 font-size: 16px; /* Slightly larger font */
             }
             
             #selected-object-color-picker {
                 width: 45px !important; /* Consistent size */
                 height: 35px !important;
                 border: 2px solid #000080 !important;
                 padding: 2px !important;
                 cursor: pointer !important;
                 border-radius: 4px !important;
             }
             
             #toggle-object-visibility {
                 padding: 6px 12px !important; /* Adjusted padding */
                 font-size: 14px !important; /* Adjusted font size */
                 background: #000080 !important;
                 color: #FFD700 !important;
                 border: 2px solid #FFD700 !important;
                 border-radius: 5px !important;
                 cursor: pointer !important;
                 transition: all 0.3s ease !important;
             }
             
             #toggle-object-visibility:hover {
                 background: #FFD700 !important;
                 color: #000080 !important;
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
             
            /* Footer styles (copied from sb.py) */
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
            
            .footer-copyright {
                margin-top: 15px;
                font-size: 14px;
                color: #cccccc;
            }

            /* Responsive styles (copied and adapted from sb.py) */
            @media (max-width: 768px) {
                 .viewer-title {
                     font-size: 48px; /* Smaller title */
                 }
                 .subtitle {
                     font-size: 36px;
                 }
                 .controls {
                     flex-direction: column;
                     gap: 10px; /* Increase gap slightly for column layout */
                     width: 100%; /* Full width on mobile */
                     padding: 0 10px; /* Add horizontal padding */
                     box-sizing: border-box;
                 }
                 .control-section {
                      width: 100%; /* Full width */
                      padding: 10px;
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
                 
                 .material-controls {
                      gap: 10px;
                 }
                 
                 .material-control {
                     min-width: 100px; /* Smaller min-width */
                     padding: 8px;
                 }

                 .material-control input[type="color"] {
                     width: 60px !important;
                     height: 40px !important;
                 }
                
                 .texture-dropdown {
                     width: 100px;
                     font-size: 12px;
                 }
                 
                 #object-interaction-area {
                     flex-direction: column; /* Stack interaction items vertically */
                     gap: 8px;
                     max-width: 90%;
                 }
                 
                 .interactive-note {
                     font-size: 16px;
                 }
                 
                  #model-groups-menu {
                     width: 200px; /* Slightly narrower menu on mobile */
                 }
                 
                  /* Adjust menu content font sizes etc. if needed for mobile */
                 #model-groups-menu h3 {
                     font-size: 14px;
                 }
                 .model-group-name {
                     font-size: 12px;
                 }
                 .model-group-controls label,
                 .model-group-controls button,
                 .model-group-controls select {
                      font-size: 11px;
                 }
            }
        </style>
    </head>
    <body>
        <a href="/" class="back-button">← Back to Home</a>

        <div class="viewer-title">
            <span class="combined-bubble-text" data-text="Interactive House Model">Interactive House Model</span>
        </div>

         <div class="subtitle">
             <span class="combined-bubble-text gold" data-text="OBJ VIEWER">OBJ VIEWER</span>
         </div>

        <!-- Copied Three.js viewer container and controls -->
        <div class="threejs-container">
            <div id="threejs-viewer">
                <!-- Menu will be added here by JS -->
            </div>
        </div>
        
        <div id="object-interaction-area">
            <span id="clicked-object-display">
                Clicked: (None)
            </span>
            <input type="color" id="selected-object-color-picker" style="display: none;">
            <button id="toggle-object-visibility" style="display: none;">Hide</button> 
        </div>
        
        <div class="controls">
            <div class="control-section">
                 <h4>Camera Controls:</h4>
                 <div class="camera-controls">
                     <label for="zoom-input">Zoom:</label>
                     <button id="zoom-out">-</button>
                     <input type="number" id="zoom-input" min="1" max="100" value="8" step="1">
                     <button id="zoom-in">+</button>
                     
                     <button id="rotate-left">Rotate Left</button>
                     <button id="rotate-right">Rotate Right</button>
                     <button id="pause-rotation">Pause</button>
                 </div>
             </div>
             
             <div class="control-section">
                 <h4>Environment Controls:</h4>
                 <div class="environment-controls">
                     <label for="lighting-intensity">Lighting:</label>
                     <input type="range" id="lighting-intensity" min="0.1" max="2.5" step="0.1" value="1.0">
                     <label for="background-color">Background:</label>
                     <input type="color" id="background-color" value="#000000">
                </div>
             </div>
        </div>
        <div class="viewer-instructions">
            <div class="interactive-note">Mouse: Click & drag to rotate. Scroll to zoom. Right-click or Shift + drag to pan.</div>
            <div class="interactive-note">Touch: One finger to rotate. Pinch to zoom. Two fingers to pan.</div>
        </div>

        <div class="footer">
            <div class="footer-content">
                <div class="footer-copyright">SERENE BUILD - IREOLUWA</div>
            </div>
        </div>

        <!-- Copied Three.js script logic -->
        <script type="module">
            import * as THREE from 'https://cdn.skypack.dev/three@0.128.0';
            import { OrbitControls } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/controls/OrbitControls.js';
            import { OBJLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/OBJLoader.js';
            import { MTLLoader } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/loaders/MTLLoader.js';
            // Removed GLTF loader import as it's not used here
            import { EffectComposer } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/EffectComposer.js';
            import { RenderPass } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/RenderPass.js';
            import { OutlinePass } from 'https://cdn.skypack.dev/three@0.128.0/examples/jsm/postprocessing/OutlinePass.js';

            let scene, camera, renderer, controls, currentModel;
            let isRotating = false;
            let rotationDirection = 0;
            
            // Store material references for easy access
            let materials = {
                'outside_walls': null,
                'interior_walls': null,
                'Garage_door': null,
                'window_glass': null,
                'interior_floor': null
            };

            // Store current texture selection globally
            let currentFloorTexture = 'wood'; // Default to wood
            let textureLoader; // Declare texture loader
            let allLights = []; // Array to store references to lights
            let initialIntensities = {}; // Store initial light intensities
            let raycaster; // Re-add for detecting clicks
            let mouse;     // Re-add for mouse coordinates
            let selectedMaterialForEditing = null; // Variable to hold the clicked material
            let selectedMeshForEditing = null; // Variable to hold the clicked mesh
            let composer; // For post-processing
            let outlinePass; // For highlighting

            function init() {
                raycaster = new THREE.Raycaster(); // Initialize Raycaster
                mouse = new THREE.Vector2();     // Initialize mouse vector
                selectedMaterialForEditing = null; // Ensure it's null on init
                selectedMeshForEditing = null; // Ensure mesh is null on init
                
                // Create scene
                scene = new THREE.Scene();
                scene.background = new THREE.Color(0x000000); // Changed to black background

                // Create camera with fixed aspect ratio
                const container = document.getElementById('threejs-viewer');
                if (!container) {
                    console.error("Viewer container not found!");
                    return;
                }
                const aspect = 16 / 12; // Match the container's aspect ratio
                camera = new THREE.PerspectiveCamera(30, aspect, 0.1, 1000);
                
                // Initialize Texture Loader
                textureLoader = new THREE.TextureLoader();

                // Create renderer with responsive sizing
                renderer = new THREE.WebGLRenderer({ antialias: true });
                renderer.setSize(container.clientWidth, container.clientWidth / aspect);
                renderer.physicallyCorrectLights = true; // Enable physically correct lighting
                renderer.shadowMap.enabled = true; // Enable shadow mapping
                renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Softer shadows
                container.appendChild(renderer.domElement);

                // Post-processing Composer Setup
                composer = new EffectComposer(renderer);
                const renderPass = new RenderPass(scene, camera);
                composer.addPass(renderPass);

                // Set up the outline pass
                outlinePass = new OutlinePass(
                    new THREE.Vector2(container.clientWidth, container.clientWidth / aspect), 
                    scene, 
                    camera
                );
                outlinePass.edgeStrength = 3.0;
                outlinePass.edgeGlow = 0.5;
                outlinePass.edgeThickness = 1.0;
                outlinePass.pulsePeriod = 0;
                outlinePass.visibleEdgeColor.set('#ffff00'); // Yellow outline
                outlinePass.hiddenEdgeColor.set('#ffff00'); // Yellow outline for hidden parts
                composer.addPass(outlinePass);

                // Add enhanced lighting setup
                const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
                scene.add(ambientLight);
                allLights.push(ambientLight);
                initialIntensities[ambientLight.uuid] = ambientLight.intensity;
                
                const directionalLight = new THREE.DirectionalLight(0xffffff, 1.5);
                directionalLight.position.set(1, 1, 1);
                directionalLight.castShadow = true; // Enable shadows for this light
                 // Configure shadow properties for directional light
                 directionalLight.shadow.mapSize.width = 1024; // default
                 directionalLight.shadow.mapSize.height = 1024; // default
                 directionalLight.shadow.camera.near = 0.5; // default
                 directionalLight.shadow.camera.far = 50; // default
                 directionalLight.shadow.camera.left = -10;
                 directionalLight.shadow.camera.right = 10;
                 directionalLight.shadow.camera.top = 10;
                 directionalLight.shadow.camera.bottom = -10;
                scene.add(directionalLight);
                allLights.push(directionalLight);
                initialIntensities[directionalLight.uuid] = directionalLight.intensity;
                
                const backLight = new THREE.DirectionalLight(0xffffff, 0.8);
                backLight.position.set(-1, 0.5, -1);
                scene.add(backLight);
                allLights.push(backLight);
                initialIntensities[backLight.uuid] = backLight.intensity;
                
                const pointLight1 = new THREE.PointLight(0xffffff, 1.0, 50); // Increased intensity
                pointLight1.position.set(5, 5, 5);
                 pointLight1.castShadow = true; // Enable shadows for point lights too
                scene.add(pointLight1);
                allLights.push(pointLight1);
                initialIntensities[pointLight1.uuid] = pointLight1.intensity;
                
                const pointLight2 = new THREE.PointLight(0xffffff, 0.8, 50);
                pointLight2.position.set(-5, 3, -5);
                 pointLight2.castShadow = true;
                scene.add(pointLight2);
                allLights.push(pointLight2);
                initialIntensities[pointLight2.uuid] = pointLight2.intensity;
                
                const pointLight3 = new THREE.PointLight(0xffffff, 0.7, 50);
                pointLight3.position.set(0, -5, 0);
                scene.add(pointLight3);
                allLights.push(pointLight3);
                initialIntensities[pointLight3.uuid] = pointLight3.intensity;

                // Add controls
                controls = new OrbitControls(camera, renderer.domElement);
                controls.enableDamping = true;
                controls.dampingFactor = 0.05;
                controls.screenSpacePanning = true; // Use true for better panning

                // Load OBJ file
                loadOBJFile('/assets/pk4.obj'); // Assumes assets folder is served correctly

                // Start animation loop
                animate();

                // Add event listeners for controls
                document.getElementById('zoom-input')?.addEventListener('input', changeZoom);
                document.getElementById('zoom-in')?.addEventListener('click', zoomIn);
                document.getElementById('zoom-out')?.addEventListener('click', zoomOut);
                document.getElementById('rotate-left')?.addEventListener('click', () => setRotation(-1));
                document.getElementById('rotate-right')?.addEventListener('click', () => setRotation(1));
                document.getElementById('pause-rotation')?.addEventListener('click', pauseRotation);
                
                // Add material color change listeners
                document.getElementById('outside-walls-color')?.addEventListener('input', (e) => changeMaterialKd('outside_walls', e.target.value));
                document.getElementById('interior-walls-color')?.addEventListener('input', (e) => changeMaterialKd('interior_walls', e.target.value));
                document.getElementById('garage-door-color')?.addEventListener('input', (e) => changeMaterialKd('Garage_door', e.target.value));
                document.getElementById('interior-floor-color')?.addEventListener('input', (e) => changeMaterialKd('interior_floor', e.target.value));
                
                // Add texture change listener
                document.getElementById('interior-floor-texture')?.addEventListener('change', changeFloorTexture);
                
                // Add event listeners for Environment controls
                document.getElementById('lighting-intensity')?.addEventListener('input', changeLightingIntensity);
                document.getElementById('background-color')?.addEventListener('input', changeBackgroundColor);

                // Add click listener for object identification and selection
                renderer.domElement.addEventListener('click', onModelClick);

                // Add listener for the selected object color picker
                document.getElementById('selected-object-color-picker')?.addEventListener('input', onSelectedColorChange);
                
                // Add listener for the visibility toggle button
                document.getElementById('toggle-object-visibility')?.addEventListener('click', onToggleVisibilityClick);
                
                // Create and add the side menu for model groups
                createModelGroupsMenu();
                
                 // Add window resize listener
                 window.addEventListener('resize', onWindowResize);
                 onWindowResize(); // Call once initially to set size
            }

            // Function to change only the Kd (diffuse color) value of a specific material
            function changeMaterialKd(materialName, colorHex) {
                const targetMaterial = materials[materialName];
                if (targetMaterial) {
                    const color = new THREE.Color(colorHex);
                    targetMaterial.color.set(color); // Set the diffuse color
                    targetMaterial.needsUpdate = true;

                    // If changing the floor color, potentially remove texture
                    if (materialName === 'interior_floor') {
                        targetMaterial.map = null; // Remove texture when color is set explicitly
                        // Update the main texture dropdown to reflect no texture
                        const textureDropdown = document.getElementById('interior-floor-texture');
                        if (textureDropdown) textureDropdown.value = ''; // Assuming you add a "None" option or handle empty value
                        currentFloorTexture = null; // Update global state
                    }

                    // Update side menu if a matching object is selected
                    if (selectedMeshForEditing && selectedMaterialForEditing === targetMaterial) {
                        const menuColorPicker = document.getElementById(`color-picker-${selectedMeshForEditing.uuid}`);
                        if (menuColorPicker) menuColorPicker.value = colorHex;
                        if (materialName === 'interior_floor') {
                            const menuTextureSelect = document.getElementById(`texture-select-${selectedMeshForEditing.uuid}`);
                            if (menuTextureSelect) menuTextureSelect.value = ''; // Reset side menu texture too
                        }
                    }
                    
                     // Update main interaction area picker if this material is selected there
                     if (selectedMaterialForEditing === targetMaterial) {
                         const interactionColorPicker = document.getElementById('selected-object-color-picker');
                         if (interactionColorPicker) interactionColorPicker.value = colorHex;
                     }
                    
                } else {
                    console.warn(`Material '${materialName}' not found in main controls mapping.`);
                }
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
                    currentModel.rotation.y += rotationDirection * 0.01;
                }
                controls.update(); // Required if damping or auto-rotation is enabled
                composer.render(); // Render using the EffectComposer
            }

            function loadOBJFile(objPath) {
                 const mtlPath = objPath.replace('.obj', '.mtl'); // Assume MTL has same name
                 const mtlLoader = new MTLLoader();
                 const objLoader = new OBJLoader();
                 
                 console.log(`Loading MTL: ${mtlPath}`);
                 mtlLoader.load(mtlPath, function(mtlMaterials) {
                     mtlMaterials.preload();
                     console.log("MTL loaded:", mtlMaterials);
                     
                     // Iterate through loaded materials to set specific properties
                     for (const materialName in materials) {
                         const currentMaterial = mtlMaterials.materials[materialName];
                         if (currentMaterial) {
                             materials[materialName] = currentMaterial; // Store reference
                             
                             // Enable shadows
                             currentMaterial.receiveShadow = true;
                             currentMaterial.castShadow = true;
                             
                             // Set initial color picker values for main controls
                             const mainColorPickerId = materialName.replace(/_/g, '-').toLowerCase() + '-color';
                             const mainColorPicker = document.getElementById(mainColorPickerId);
                             if (mainColorPicker) {
                                 mainColorPicker.value = '#' + currentMaterial.color.getHexString();
                             } else if (materialName !== 'window_glass') { // Don't warn for glass as it has no main picker
                                 console.warn(`Main color picker '${mainColorPickerId}' not found.`);
                             }
                             
                             // Enhance glass material
                             if (materialName === 'window_glass') {
                                 currentMaterial.transparent = true;
                                 currentMaterial.opacity = 0.5; // More transparent glass
                                 currentMaterial.shininess = 100;
                                 currentMaterial.specular = new THREE.Color(0xeeeeee); // Slightly less intense specular
                                 currentMaterial.refractionRatio = 0.98;
                                 currentMaterial.side = THREE.DoubleSide; // Render both sides for glass panes
                                 currentMaterial.castShadow = false; // Glass usually doesn't cast strong shadows
                                 // Ensure depthWrite is false for transparent materials to render correctly
                                 currentMaterial.depthWrite = false; 
                                 currentMaterial.depthTest = true; // Still test depth
                                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
                             }
                             
                             // Setup default floor texture
                             else if (materialName === 'interior_floor') {
                                 currentMaterial.shininess = 30;
                                 currentMaterial.specular = new THREE.Color(0x222222);
                                 applyTextureToMaterial(currentMaterial, currentFloorTexture); // Apply default texture
                                 // Ensure floor is opaque and writes to depth buffer
                                 currentMaterial.transparent = false;
                                 currentMaterial.depthWrite = true;
                                 currentMaterial.depthTest = true;
                                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
                             }
                             else {
                                 // For all other materials, ensure they are opaque and write depth
                                 currentMaterial.transparent = false;
                                 currentMaterial.depthWrite = true;
                                 currentMaterial.depthTest = true;
                                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
                             }
                         }
                     }
                     
                     // Also iterate through all loaded materials for general setup (like shadows)
                     // This ensures materials not in our main `materials` object are also processed
                     Object.keys(mtlMaterials.materials).forEach(loadedMatName => {
                          const loadedMat = mtlMaterials.materials[loadedMatName];
                          if (loadedMat && !materials[loadedMatName]) { // Process if not already handled above
                              loadedMat.receiveShadow = true;
                              loadedMat.castShadow = true;
                              loadedMat.transparent = false;
                              loadedMat.depthWrite = true;
                              loadedMat.depthTest = true;
                              loadedMat.alphaTest = 0.5;
                              loadedMat.side = THREE.FrontSide;
                          }
                     });
                     
                     objLoader.setMaterials(mtlMaterials);
                     console.log(`Loading OBJ: ${objPath}`);
                     objLoader.load(objPath, function(object) {
                         console.log("OBJ loaded:", object);
                         
                          // Enable shadows for all meshes in the loaded object
                          object.traverse(function (child) {
                              if (child.isMesh) {
                                  child.castShadow = true;
                                  child.receiveShadow = true;
                              }
                          });
                          
                         // Center and scale
                         const box = new THREE.Box3().setFromObject(object);
                         const center = box.getCenter(new THREE.Vector3());
                         const size = box.getSize(new THREE.Vector3());
                         const maxDim = Math.max(size.x, size.y, size.z);
                         const scale = 7 / maxDim; // Adjust scale factor if needed
                         object.scale.set(scale, scale, scale);
                         object.position.sub(center.multiplyScalar(scale));
                         
                         // Add to scene
                         if (currentModel) { // Remove previous model if reloading
                             scene.remove(currentModel);
                         }
                         scene.add(object);
                         currentModel = object;
                         
                         // Populate the groups menu
                         populateModelGroupsMenu();

                         // Set initial camera position
                         camera.position.set(0, 2, 8.0); // Slightly higher Y position
                         controls.target.set(0, 0, 0); // Look at the center
                         controls.update();
                         
                         // Ensure controls know the new target
                          controls.target.copy(object.position);
                          controls.update();

                     }, undefined, (error) => {
                          console.error("Error loading OBJ file:", error);
                     });
                 }, undefined, (error) => {
                     console.error("Error loading MTL file:", error);
                     // Optionally, try loading OBJ without MTL
                     // objLoader.load(objPath, function(object) { ... });
                 });
            }

            function changeZoom(event) {
                 const zoomLevel = parseFloat(event.target.value);
                 // Adjust camera distance instead of just Z position for perspective camera
                 const direction = new THREE.Vector3();
                 camera.getWorldDirection(direction);
                 const currentDistance = camera.position.distanceTo(controls.target);
                 // Calculate the new position along the view direction
                 // This is a simplification; OrbitControls handles zoom more complexly.
                 // We'll directly manipulate controls zoom/distance if possible, or just Z.
                 camera.position.z = zoomLevel; // Simple Z adjustment remains
                 controls.update();
             }
             
             function zoomIn() {
                 const slider = document.getElementById('zoom-input');
                 if (!slider) return;
                 let currentZoom = parseFloat(slider.value);
                 let newZoom = Math.max(parseFloat(slider.min), currentZoom - parseFloat(slider.step || 1)); // Use step value
                 slider.value = newZoom;
                 camera.position.z = newZoom; // Adjust Z
                 controls.update();
             }

             function zoomOut() {
                 const slider = document.getElementById('zoom-input');
                 if (!slider) return;
                 let currentZoom = parseFloat(slider.value);
                 let newZoom = Math.min(parseFloat(slider.max), currentZoom + parseFloat(slider.step || 1)); // Use step value
                 slider.value = newZoom;
                 camera.position.z = newZoom; // Adjust Z
                 controls.update();
             }
             
             // Function to apply texture based on type string
            function applyTextureToMaterial(material, textureType) {
                if (!material) {
                    console.warn("Attempted to apply texture to null material.");
                    return;
                }
                let texturePath = '';
                let repeatFactor = 1; // Default repeat factor

                switch (textureType) {
                    case 'wood': texturePath = '/assets/floor.jpg'; repeatFactor = 2; break;
                    case 'carpet': texturePath = '/assets/carpet.jpg'; repeatFactor = 3; break;
                    case 'porcelain': texturePath = '/assets/porcelain.jpg'; repeatFactor = 2; break;
                    case 'epoxy': texturePath = '/assets/600-epoxy-flooring-ideas-sample.jpg'; repeatFactor = 1; break;
                    case 'concrete': texturePath = '/assets/360_F_310285583_ILKFCwTerYFhqcIGiNL9zuY68sy7xd16.jpg'; repeatFactor = 2; break;
                    default:
                        console.warn("Unknown or null texture type specified:", textureType);
                        material.map = null;
                        material.transparent = false; // Ensure opaque if texture removed
                        material.depthWrite = true;
                        material.depthTest = true;
                        material.alphaTest = 0.5;
                        material.needsUpdate = true;
                        return;
                }

                console.log(`Applying texture: ${texturePath} for type ${textureType}`);
                textureLoader.load(
                    texturePath,
                    (texture) => {
                         console.log(`Texture loaded: ${texturePath}`);
                         texture.wrapS = THREE.RepeatWrapping;
                         texture.wrapT = THREE.RepeatWrapping;
                         texture.repeat.set(repeatFactor, repeatFactor);
                         
                         material.map = texture;
                         material.color.set(0xFFFFFF); // Reset color to show texture fully
                         material.transparent = false; // Force opaque
                         material.depthWrite = true;
                         material.depthTest = true;
                         material.alphaTest = 0.5; // Keep high alpha test
                         material.needsUpdate = true;
                         console.log(`Texture applied to material. Map:`, material.map);
                    },
                    undefined,
                    (error) => {
                        console.error(`Error loading texture: ${texturePath}`, error);
                        material.map = null;
                        material.needsUpdate = true;
                    }
                );
            }

            // Event handler for main floor texture dropdown change
            function changeFloorTexture(event) {
                const textureType = event.target.value;
                currentFloorTexture = textureType; // Update global state
                
                const floorMaterial = materials['interior_floor'];
                if (floorMaterial) {
                    applyTextureToMaterial(floorMaterial, textureType);
                    
                    // Reset the main floor color picker to white
                    const mainFloorColorPicker = document.getElementById('interior-floor-color');
                    if (mainFloorColorPicker) mainFloorColorPicker.value = "#ffffff";

                    // Update side menu if a floor object is selected
                    if (selectedMeshForEditing && selectedMaterialForEditing === floorMaterial) {
                        const menuTextureSelect = document.getElementById(`texture-select-${selectedMeshForEditing.uuid}`);
                        if (menuTextureSelect) menuTextureSelect.value = textureType || '';
                        const menuColorPicker = document.getElementById(`color-picker-${selectedMeshForEditing.uuid}`);
                        if (menuColorPicker) menuColorPicker.value = "#ffffff"; // Reset menu color too
                    }
                } else {
                    console.warn("Interior floor material reference not found.");
                }
            }

            // Function to change lighting intensity
            function changeLightingIntensity(event) {
                const multiplier = parseFloat(event.target.value);
                allLights.forEach(light => {
                    if (initialIntensities[light.uuid] !== undefined) {
                        light.intensity = initialIntensities[light.uuid] * multiplier;
                    }
                });
            }

            // Function to change background color
            function changeBackgroundColor(event) {
                const color = new THREE.Color(event.target.value);
                scene.background = color;
            }

            // Click handler for object selection
            function onModelClick(event) {
                const displayElement = document.getElementById('clicked-object-display');
                const colorPicker = document.getElementById('selected-object-color-picker');
                const visibilityButton = document.getElementById('toggle-object-visibility');
                
                // Calculate mouse position in normalized device coordinates (-1 to +1) for component
                const rect = renderer.domElement.getBoundingClientRect();
                mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
                mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
                
                raycaster.setFromCamera(mouse, camera);

                let intersects = [];
                if (currentModel) {
                    intersects = raycaster.intersectObject(currentModel, true); // Check descendants
                }

                // Reset previous selection visuals
                outlinePass.selectedObjects = [];
                selectedMeshForEditing = null;
                selectedMaterialForEditing = null;
                colorPicker.style.display = 'none';
                visibilityButton.style.display = 'none';
                displayElement.textContent = 'Clicked: (None)';
                 document.querySelectorAll('.model-group-item').forEach(item => {
                     item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)'; // Reset menu item background
                 });

                if (intersects.length > 0) {
                    const intersection = intersects[0];
                    const object = intersection.object; // The intersected mesh
                    
                    if (object instanceof THREE.Mesh) {
                        selectedMeshForEditing = object;
                        outlinePass.selectedObjects = [selectedMeshForEditing]; // Highlight
                        
                        // Determine the target material
                        let targetMaterial;
                        if (Array.isArray(object.material)) {
                            // If multi-material, use the material index from the intersection face
                            if (intersection.face && intersection.face.materialIndex !== undefined && object.material[intersection.face.materialIndex]) {
                                targetMaterial = object.material[intersection.face.materialIndex];
                            } else {
                                targetMaterial = object.material[0]; // Fallback to first material
                                console.warn("Multi-material mesh clicked, but couldn't determine specific material from face. Using first material.");
                            }
                        } else {
                            // Single material
                            targetMaterial = object.material;
                        }

                        if (targetMaterial) {
                            selectedMaterialForEditing = targetMaterial;
                            const objectName = getHierarchicalName(object); // Use helper for better name
                            displayElement.textContent = `Selected: ${objectName}`;
                            
                            // Update and show controls
                            colorPicker.value = `#${selectedMaterialForEditing.color.getHexString()}`;
                            colorPicker.style.display = 'inline-block';
                            
                            visibilityButton.textContent = selectedMeshForEditing.visible ? 'Hide' : 'Show';
                            visibilityButton.style.display = 'inline-block';
                            
                            // Highlight and scroll to the corresponding menu item
                            highlightMenuItem(objectName);
                             console.log("Selected mesh:", selectedMeshForEditing);
                             console.log("Selected material:", selectedMaterialForEditing);
                        } else {
                            displayElement.textContent = `Clicked: ${getHierarchicalName(object)} (No material)`;
                        }
                    } else {
                         // Might have clicked a line or point
                         displayElement.textContent = `Clicked: (Not a mesh - ${object.type})`;
                    }
                }
            }
            
             // Helper to get a more descriptive name including parents
             function getHierarchicalName(obj) {
                 if (!obj) return 'Unknown';
                 let name = obj.name || 'Unnamed';
                 let parent = obj.parent;
                 let depth = 0;
                 while (parent && !(parent instanceof THREE.Scene) && depth < 5) {
                     if (parent.name) {
                         name = `${parent.name} > ${name}`;
                     }
                     parent = parent.parent;
                     depth++;
                 }
                 return name;
             }
             
             // Helper function to find and highlight menu item
             function highlightMenuItem(objectName) {
                  const menuItems = document.querySelectorAll('.model-group-item');
                  let foundItem = null;
                  menuItems.forEach(item => {
                       const nameElement = item.querySelector('.model-group-name'); // Use updated class
                       if (nameElement && nameElement.textContent === objectName) {
                           item.style.backgroundColor = 'rgba(80, 80, 80, 0.9)'; // Highlight color
                            foundItem = item;
                       } else {
                            item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)'; // Reset others
                       }
                  });
                  
                  // Scroll the menu if the item was found
                  if (foundItem) {
                       const menuContainer = document.getElementById('model-groups-menu');
                       if (menuContainer) {
                            foundItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
                       }
                  }
             }


            // Handler for color change from the selected object picker
            function onSelectedColorChange(event) {
                if (selectedMaterialForEditing) {
                    const newColor = new THREE.Color(event.target.value);
                    selectedMaterialForEditing.color.set(newColor);
                    selectedMaterialForEditing.needsUpdate = true;
                    console.log(`Set selected material color to ${event.target.value}`);
                    
                    // Update the corresponding color picker in the side menu if it exists
                     if (selectedMeshForEditing) {
                          const menuColorPicker = document.getElementById(`color-picker-${selectedMeshForEditing.uuid}`);
                          if (menuColorPicker) {
                              menuColorPicker.value = event.target.value;
                          }
                           // If it's a floor, also reset the texture dropdown in the menu
                          if (selectedMeshForEditing.name.toLowerCase().includes('floor')) {
                               const menuTextureSelect = document.getElementById(`texture-select-${selectedMeshForEditing.uuid}`);
                               if (menuTextureSelect) {
                                    menuTextureSelect.value = ''; // Or a 'none' option if you add one
                               }
                          }
                     }
                } else {
                     console.warn("Color changed but no material selected.");
                }
            }

            // Handler for visibility toggle button
            function onToggleVisibilityClick() {
                if (selectedMeshForEditing) {
                    selectedMeshForEditing.visible = !selectedMeshForEditing.visible;
                    const visibilityButton = document.getElementById('toggle-object-visibility');
                    visibilityButton.textContent = selectedMeshForEditing.visible ? 'Hide' : 'Show';
                    console.log(`Toggled visibility for ${getHierarchicalName(selectedMeshForEditing)}. Now visible: ${selectedMeshForEditing.visible}`);
                    
                    // Update the corresponding visibility button in the side menu if it exists
                     const menuVisButton = document.getElementById(`vis-button-${selectedMeshForEditing.uuid}`);
                     if (menuVisButton) {
                          menuVisButton.textContent = selectedMeshForEditing.visible ? 'Hide' : 'Show';
                          // Optionally add a visual cue like strikethrough or dimming in the menu
                           const groupItem = menuVisButton.closest('.model-group-item');
                           if (groupItem) {
                                groupItem.style.opacity = selectedMeshForEditing.visible ? '1' : '0.5';
                           }
                     }
                } else {
                    console.warn("Toggle visibility clicked, but no mesh selected.");
                }
            }

             // Function to create the collapsible model groups menu
            function createModelGroupsMenu() {
                const viewerContainer = document.getElementById('threejs-viewer');
                if (!viewerContainer) return; // Don't create if container doesn't exist

                // Remove existing menu if any
                const existingMenu = document.getElementById('model-groups-menu');
                if (existingMenu) {
                    existingMenu.remove();
                }
                
                const menuContainer = document.createElement('div');
                menuContainer.id = 'model-groups-menu';
                // Styles are applied via CSS now
                
                // Header with collapse button
                const header = document.createElement('div');
                 header.id = 'model-menu-header'; // Use specific ID
                 // Styles applied via CSS
                
                const title = document.createElement('h3');
                title.textContent = 'Model Objects'; // Changed title
                title.style.margin = '0';
                
                const collapseBtn = document.createElement('button');
                collapseBtn.id = 'model-menu-collapse-btn'; // Use specific ID
                collapseBtn.innerHTML = '&minus;'; // Initial state: visible
                 // Styles applied via CSS
                
                collapseBtn.addEventListener('click', () => {
                    const isCollapsed = menuContainer.dataset.collapsed === 'true';
                    if (isCollapsed) {
                        menuContainer.style.transform = 'translateX(0)';
                        menuContainer.dataset.collapsed = 'false';
                        collapseBtn.innerHTML = '&minus;';
                    } else {
                        // Calculate translate based on actual width to hide most of it
                         const menuWidth = menuContainer.offsetWidth;
                         const hiddenWidth = Math.max(0, menuWidth - 30); // Keep 30px visible
                         menuContainer.style.transform = `translateX(-${hiddenWidth}px)`;
                         menuContainer.dataset.collapsed = 'true';
                        collapseBtn.innerHTML = '&plus;';
                    }
                });
                
                header.appendChild(title);
                header.appendChild(collapseBtn);
                menuContainer.appendChild(header);
                
                // Container for group items
                const groupsContainer = document.createElement('div');
                groupsContainer.id = 'model-groups-container';
                menuContainer.appendChild(groupsContainer);
                
                viewerContainer.appendChild(menuContainer); // Add to viewer
                
                // Populate if model already loaded
                if (currentModel) {
                    populateModelGroupsMenu();
                }
            }
            
            // Function to populate the model groups menu
            function populateModelGroupsMenu() {
                const groupsContainer = document.getElementById('model-groups-container');
                if (!groupsContainer) {
                     console.error("Required container element 'model-groups-container' not found.");
                     return;
                }
                
                groupsContainer.innerHTML = ''; // Clear existing side menu entries
                
                if (!currentModel) return;
                
                const groupsMap = new Map();
                
                // Traverse to find all unique meshes and group them loosely by name/parent
                 currentModel.traverse((node) => {
                     if (node instanceof THREE.Mesh) {
                         const hierarchicalName = getHierarchicalName(node);
                         
                         // Use hierarchical name as the key to avoid duplicates from complex scenes
                         if (!groupsMap.has(hierarchicalName)) {
                             groupsMap.set(hierarchicalName, node);
                         }
                     }
                 });
                 
                // Sort groups alphabetically by name
                const sortedGroups = Array.from(groupsMap.entries()).sort((a, b) => a[0].localeCompare(b[0]));
                
                // Create UI for each group/mesh
                sortedGroups.forEach(([name, node]) => {
                    const groupItem = document.createElement('div');
                    groupItem.className = 'model-group-item';
                     groupItem.style.opacity = node.visible ? '1' : '0.5'; // Reflect initial visibility
                    // Styles applied via CSS
                    
                    // Header part (Icon + Name) - clickable for selection
                    const groupHeader = document.createElement('div');
                    groupHeader.className = 'model-group-header'; // Use specific class
                    // Styles applied via CSS
                    
                    const groupIcon = document.createElement('div');
                    groupIcon.className = 'model-group-icon'; // Use specific class
                    groupIcon.innerHTML = '&#9632;'; // Cube symbol
                    // Styles applied via CSS
                    
                    const groupName = document.createElement('div');
                    groupName.className = 'model-group-name'; // Use specific class
                    groupName.textContent = name;
                    groupName.title = name; // Show full name on hover if truncated
                    // Styles applied via CSS
                    
                    groupHeader.appendChild(groupIcon);
                    groupHeader.appendChild(groupName);
                    
                    // Click on header selects the object
                    groupHeader.addEventListener('click', () => {
                         // Simulate clicking the object in the 3D view
                         // This reuses the selection logic for consistency
                         selectObjectFromMenu(node);
                    });
                    
                    groupItem.appendChild(groupHeader);
                    
                    // Controls container (Color, Texture, Visibility)
                    const controlsContainer = document.createElement('div');
                    controlsContainer.className = 'model-group-controls'; // Use specific class
                    // Styles applied via CSS
                    
                    // Color Picker
                    const colorPicker = document.createElement('input');
                    colorPicker.type = 'color';
                    colorPicker.id = `color-picker-${node.uuid}`; // Unique ID based on UUID
                    colorPicker.value = '#ffffff'; // Default
                     // Get current color from the primary material
                    const primaryMaterial = Array.isArray(node.material) ? node.material[0] : node.material;
                    if (primaryMaterial && primaryMaterial.color) {
                        colorPicker.value = '#' + primaryMaterial.color.getHexString();
                    }
                    // Styles applied via CSS
                    
                    colorPicker.addEventListener('input', (e) => {
                        const color = new THREE.Color(e.target.value);
                        
                        // Apply color to all materials of the mesh
                        const materialsToUpdate = Array.isArray(node.material) ? node.material : [node.material];
                        materialsToUpdate.forEach(mat => {
                            if (mat) {
                                 mat.color.set(color);
                                 mat.needsUpdate = true;
                            }
                        });
                        
                         // If this node is currently selected, update the main color picker too
                         if (selectedMeshForEditing === node) {
                              const mainColorPicker = document.getElementById('selected-object-color-picker');
                              if (mainColorPicker) mainColorPicker.value = e.target.value;
                         }
                          // If it's a floor, reset texture dropdown
                         if (name.toLowerCase().includes('floor')) {
                              const textureSelect = document.getElementById(`texture-select-${node.uuid}`);
                              if (textureSelect) textureSelect.value = ''; // Reset dropdown
                              
                               // If this is the main floor, reset the main dropdown too
                              if (node.material === materials['interior_floor'] || (Array.isArray(node.material) && node.material.includes(materials['interior_floor']))) {
                                   const mainTextureSelect = document.getElementById('interior-floor-texture');
                                   if (mainTextureSelect) mainTextureSelect.value = '';
                              }
                         }
                    });
                    controlsContainer.appendChild(colorPicker);
                    
                    // Texture Selector (only for items named 'floor')
                    if (name.toLowerCase().includes('floor')) {
                        const textureContainer = document.createElement('div');
                        // Styles applied via CSS
                        
                        const textureLabel = document.createElement('label');
                        textureLabel.textContent = 'Texture:';
                        textureLabel.setAttribute('for', `texture-select-${node.uuid}`);
                        // Styles applied via CSS
                        
                        const textureSelect = document.createElement('select');
                        textureSelect.id = `texture-select-${node.uuid}`; // Unique ID
                        // Styles applied via CSS
                        
                        // Add texture options
                        const textureOptions = [
                            { value: '', text: 'None' }, // Option to remove texture
                            { value: 'wood', text: 'Wood' },
                            { value: 'carpet', text: 'Carpet' },
                            { value: 'porcelain', text: 'Porcelain' },
                            { value: 'epoxy', text: 'Epoxy' },
                            { value: 'concrete', text: 'Concrete' }
                        ];
                        
                        textureOptions.forEach(opt => {
                            const optionElement = document.createElement('option');
                            optionElement.value = opt.value;
                            optionElement.textContent = opt.text;
                            textureSelect.appendChild(optionElement);
                        });
                        
                        // Set initial value based on current material's map or global floor texture
                        const currentMaterial = Array.isArray(node.material) ? node.material[0] : node.material;
                        if (currentMaterial && currentMaterial.map && currentMaterial.map.source && currentMaterial.map.source.data) {
                            const currentTextureSrc = currentMaterial.map.image?.src || '';
                            // Infer type from src (this is brittle, depends on filenames)
                            if (currentTextureSrc.includes('floor.jpg')) textureSelect.value = 'wood';
                            else if (currentTextureSrc.includes('carpet.jpg')) textureSelect.value = 'carpet';
                            else if (currentTextureSrc.includes('porcelain.jpg')) textureSelect.value = 'porcelain';
                            else if (currentTextureSrc.includes('epoxy')) textureSelect.value = 'epoxy'; // Looser match for epoxy sample
                            else if (currentTextureSrc.includes('concrete')) textureSelect.value = 'concrete'; // Looser match for concrete
                            else textureSelect.value = '';
                        } else if (node.material === materials['interior_floor'] || (Array.isArray(node.material) && node.material.includes(materials['interior_floor']))) {
                             // If it's the main floor material, use the global setting
                              textureSelect.value = currentFloorTexture || '';
                        } else {
                            textureSelect.value = ''; // Default to None
                        }
                        
                        textureSelect.addEventListener('change', (e) => {
                            const textureType = e.target.value;
                            const materialsToUpdate = Array.isArray(node.material) ? node.material : [node.material];
                            
                            materialsToUpdate.forEach(mat => {
                                 if (mat) {
                                      if (textureType) {
                                           applyTextureToMaterial(mat, textureType);
                                      } else {
                                           // Remove texture if 'None' is selected
                                           mat.map = null;
                                           mat.needsUpdate = true;
                                      }
                                 }
                            });
                            
                            // Reset the color picker for this item to white when texture changes
                            const itemColorPicker = document.getElementById(`color-picker-${node.uuid}`);
                            if (itemColorPicker) itemColorPicker.value = '#ffffff';
                            
                             // If this node is currently selected, update the main controls too
                             if (selectedMeshForEditing === node) {
                                  const mainColorPicker = document.getElementById('selected-object-color-picker');
                                  if (mainColorPicker) mainColorPicker.value = '#ffffff'; // Also reset main picker
                             }
                             
                             // If this is the main floor, update the main texture dropdown
                            if (node.material === materials['interior_floor'] || (Array.isArray(node.material) && node.material.includes(materials['interior_floor']))) {
                                 const mainTextureSelect = document.getElementById('interior-floor-texture');
                                 if (mainTextureSelect) mainTextureSelect.value = textureType;
                                 currentFloorTexture = textureType; // Update global state
                            }
                        });
                        
                        textureContainer.appendChild(textureLabel);
                        textureContainer.appendChild(textureSelect);
                        controlsContainer.appendChild(textureContainer);
                    }
                    
                    // Visibility Toggle Button
                    const visibilityBtn = document.createElement('button');
                    visibilityBtn.id = `vis-button-${node.uuid}`; // Unique ID
                    visibilityBtn.textContent = node.visible ? 'Hide' : 'Show';
                    // Styles applied via CSS
                    
                    visibilityBtn.addEventListener('click', () => {
                        node.visible = !node.visible;
                        visibilityBtn.textContent = node.visible ? 'Hide' : 'Show';
                        groupItem.style.opacity = node.visible ? '1' : '0.5'; // Update item opacity
                        
                        // If this node is currently selected, update the main visibility button too
                        if (selectedMeshForEditing === node) {
                            const mainVisButton = document.getElementById('toggle-object-visibility');
                            if (mainVisButton) mainVisButton.textContent = node.visible ? 'Hide' : 'Show';
                        }
                    });
                    
                    controlsContainer.appendChild(visibilityBtn);
                    groupItem.appendChild(controlsContainer);
                    groupsContainer.appendChild(groupItem);
                });
                
                // Message if no groups found
                if (sortedGroups.length === 0) {
                    const noGroupsMsg = document.createElement('p');
                    noGroupsMsg.textContent = 'No distinct objects found in model.';
                    noGroupsMsg.style.fontStyle = 'italic';
                     noGroupsMsg.style.padding = '10px';
                     noGroupsMsg.style.textAlign = 'center';
                    groupsContainer.appendChild(noGroupsMsg);
                }
            }
            
             // Function to programmatically select an object (e.g., when clicked in the menu)
            function selectObjectFromMenu(node) {
                 if (!(node instanceof THREE.Mesh)) return;
                 
                 // Reset previous selection visuals
                 outlinePass.selectedObjects = [];
                 document.querySelectorAll('.model-group-item').forEach(item => {
                     item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)';
                 });
                 
                 // Set new selection
                 selectedMeshForEditing = node;
                 outlinePass.selectedObjects = [node];
                 
                 // Determine material (use primary if multi-material)
                 const primaryMaterial = Array.isArray(node.material) ? node.material[0] : node.material;
                 selectedMaterialForEditing = primaryMaterial || null;
                 
                 const objectName = getHierarchicalName(node);
                 
                 // Update main interaction area display
                 const displayElement = document.getElementById('clicked-object-display');
                 const colorPicker = document.getElementById('selected-object-color-picker');
                 const visibilityButton = document.getElementById('toggle-object-visibility');
                 
                 displayElement.textContent = `Selected: ${objectName}`;
                 
                 if (selectedMaterialForEditing) {
                     colorPicker.value = '#' + selectedMaterialForEditing.color.getHexString();
                     colorPicker.style.display = 'inline-block';
                 } else {
                     colorPicker.style.display = 'none';
                 }
                 
                 visibilityButton.textContent = node.visible ? 'Hide' : 'Show';
                 visibilityButton.style.display = 'inline-block';
                 
                 // Highlight the item in the menu
                 highlightMenuItem(objectName); // This also handles scrolling
            }
            
             // Handle window resize
             function onWindowResize() {
                 const container = document.getElementById('threejs-viewer');
                 if (!container || !renderer || !composer || !camera) return;
                 
                 const aspect = 16 / 12;
                 const newWidth = container.clientWidth;
                 const newHeight = newWidth / aspect;
                 
                 camera.aspect = aspect; // Keep aspect ratio consistent
                 camera.updateProjectionMatrix();
                 
                 renderer.setSize(newWidth, newHeight);
                 composer.setSize(newWidth, newHeight); // Update composer size too
                 outlinePass.resolution.set(newWidth, newHeight); // Update outline pass resolution
             }

            // Initialize viewer when the DOM is ready
            document.addEventListener('DOMContentLoaded', init);

        </script>
    </body>
    </html>
    """
    return render_template_string(html) 