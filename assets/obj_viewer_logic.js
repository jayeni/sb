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

// REMOVED: materials object
// REMOVED: currentFloorTexture variable
let textureLoader; // Declare texture loader
let allLights = []; // Array to store references to lights
let initialIntensities = {}; // Store initial light intensities
let raycaster; // Re-add for detecting clicks
let mouse;     // Re-add for mouse coordinates
let selectedMaterialForEditing = null; // Variable to hold the clicked material
let selectedMeshForEditing = null; // Variable to hold the clicked mesh
// REMOVE Emissive highlight variables
// let originalEmissiveColors = new Map(); 
// const highlightEmissiveColor = new THREE.Color(0xffff00); 
// RESTORE composer and outlinePass variables
let composer;
let outlinePass;
let currentLightMultiplier = 1.0; // Track current overall multiplier
const lightIntensityStep = 0.1;
const minLightIntensity = 0.1;
const maxLightIntensity = 2.5; // Max multiplier

// Available flooring textures from model_images directory
let flooringTextures = [];

// Function to apply texture to material
function applyTextureToMaterial(material, textureType) {
    if (!material || !textureLoader) return;
    
    // Find matching texture based on name
    const matchingTexture = flooringTextures.find(texture => 
        texture.value === textureType || 
        (texture.fileName && texture.fileName.toLowerCase().includes(textureType.toLowerCase()))
    );
    
    if (matchingTexture) {
        const texturePath = `/assets/model_images/${matchingTexture.fileName}`;
        console.log(`Applying texture: ${texturePath}`);
        
        textureLoader.load(texturePath, (texture) => {
            texture.wrapS = THREE.RepeatWrapping;
            texture.wrapT = THREE.RepeatWrapping;
            texture.repeat.set(2, 2); // Better tiling for floor textures
            
            // Keep track of the current texture for comparing later
            texture.userData = { 
                textureType: textureType,
                fileName: matchingTexture.fileName 
            };
            
            material.map = texture;
            material.needsUpdate = true;
        }, 
        // onProgress callback - can be used for loading indicator
        undefined, 
        // onError callback
        (error) => {
            console.error(`Error loading texture ${texturePath}:`, error);
            material.map = null;
            material.needsUpdate = true;
        });
    } else {
        console.warn(`Texture not found: ${textureType}`);
        material.map = null;
        material.needsUpdate = true;
    }
}

// Load available flooring textures function
function loadFlooringTextures() {
    // Since directory listing might not be supported, we'll directly scan the model_images
    // directory for files with "_flooring" in their names by listing known files.
    
    // Check if any flooring textures exist in assets/model_images
    fetch('/assets/model_images/wooden_flooring.jpg', { method: 'HEAD' })
        .then(response => {
            // If we can access the model_images directory directly, use that path
            const basePath = '/assets/model_images/';
            
            // Manually check for known flooring texture files
            // This is a fallback approach since directory listing may not be supported
            const knownTextureFiles = [
                'wooden_flooring.jpg',
                'carpet_flooring.jpg',
                'porcelain_flooring.jpg',
                'epoxy_flooring.jpg',
                'concrete_flooring.jpg',
                'wooden_flooring_1.jpg',
                'wooden_flooring_4.jpg',
                'asphalt.jpg' // Not flooring but included if used
            ];
            
            flooringTextures = [];
            
            // Process each known file
            knownTextureFiles.forEach(fileName => {
                // Only include files with "_flooring" in the name as per requirements
                if (fileName.includes('_flooring') || fileName === 'asphalt.jpg') {
                    // Extract display name from filename
                    let displayName = fileName.replace(/\.[^/.]+$/, '').replace('_flooring', '');
                    displayName = displayName.replace(/_/g, ' ');
                    displayName = displayName.replace(/\b\w/g, c => c.toUpperCase());
                    
                    // Create value from the base name
                    const value = displayName.toLowerCase();
                    
                    flooringTextures.push({
                        fileName,
                        text: displayName || 'Texture',
                        value: value || fileName.split('.')[0]
                    });
                    
                    // Preload the texture to ensure it's available
                    textureLoader.load(basePath + fileName, 
                        texture => console.log(`Preloaded texture: ${fileName}`),
                        undefined,
                        error => console.warn(`Could not preload texture: ${fileName}`, error)
                    );
                }
            });
            
            console.log('Available flooring textures:', flooringTextures);
        })
        .catch(error => {
            console.error('Error checking model_images directory:', error);
            // Fallback to default textures
            flooringTextures = [
                { fileName: 'wooden_flooring.jpg', text: 'Wood', value: 'wood' },
                { fileName: 'carpet_flooring.jpg', text: 'Carpet', value: 'carpet' },
                { fileName: 'porcelain_flooring.jpg', text: 'Porcelain', value: 'porcelain' },
                { fileName: 'epoxy_flooring.jpg', text: 'Epoxy', value: 'epoxy' },
                { fileName: 'concrete_flooring.jpg', text: 'Concrete', value: 'concrete' }
            ];
        });
}

// --- Room Visibility --- 
const roomPrefixes = [
    "Bedroom_1", "Bedroom_2", "Bathroom", "Kitchen", 
    "Living_Room", "Garage", "Dining_Room", "Hallway"
];
let roomMeshesMap = new Map(); // Map prefix -> Set<THREE.Mesh>
const MISC_CATEGORY = "Misc"; // Category for objects not matching any room prefix
// --- End Room Visibility ---

// List of available objects for the library
const availableObjects = [
    { name: 'Cube', type: 'shape', icon: 'fas fa-cube', color: 0x3366FF },
    { name: 'Sphere', type: 'shape', icon: 'fas fa-globe', color: 0xFF6633 },
    { name: 'Cylinder', type: 'shape', icon: 'fas fa-battery-full fa-rotate-90', color: 0x66CC33 },
    { name: 'Cone', type: 'shape', icon: 'fas fa-chess-pawn', color: 0xFF3366 },
    { name: 'Torus', type: 'shape', icon: 'fas fa-circle-notch', color: 0xFFCC33 },
    { name: 'Pyramid', type: 'shape', icon: 'fas fa-triangle', color: 0x33CCFF },
    { name: 'Trapezoid', type: 'shape', icon: 'fas fa-draw-polygon', color: 0xCC33FF }
];

// Drag and drop variables
let isDragging = false;
let draggedObject = null;
let dropIndicator = null;

// Object manipulation variables
let isTransforming = false;
let transformType = null; // 'rotate' or 'move'
let transformAxis = null; // 'x', 'y', or 'z'
let transformStartPosition = new THREE.Vector2();
let transformStep = 0.1; // How much to move/rotate per pixel of mouse movement

// Initialize the viewer
function initViewer() {
    raycaster = new THREE.Raycaster(); // Initialize Raycaster
    mouse = new THREE.Vector2();     // Initialize mouse vector
    selectedMaterialForEditing = null; // Ensure it's null on init
    selectedMeshForEditing = null; // Ensure mesh is null on init
    
    // Create scene
    scene = new THREE.Scene();
    scene.background = new THREE.Color(0x000000); // Changed to black background
    scene.fog = null; // Explicitly disable fog

    // Create camera with fixed aspect ratio
    const container = document.getElementById('threejs-viewer');
    if (!container) {
        console.error("Viewer container not found!");
        return;
    }
    const aspect = 16 / 12; // Match the container's aspect ratio
    camera = new THREE.PerspectiveCamera(30, aspect, 1.0, 10000); // Increased near plane + far plane
    
    // Initialize Texture Loader
    textureLoader = new THREE.TextureLoader();
    
    // Load available flooring textures
    loadFlooringTextures();

    // Create renderer with responsive sizing
    renderer = new THREE.WebGLRenderer({ 
        antialias: true, 
        logarithmicDepthBuffer: true // Improve depth precision
    });
    renderer.setSize(container.clientWidth, container.clientWidth / aspect);
    renderer.physicallyCorrectLights = true; // Enable physically correct lighting
    renderer.shadowMap.enabled = true; // Enable shadow mapping
    renderer.shadowMap.type = THREE.PCFSoftShadowMap; // Softer shadows
    container.appendChild(renderer.domElement);

    // RESTORE Post-processing Composer and OutlinePass Setup
    composer = new EffectComposer(renderer);
    const renderPass = new RenderPass(scene, camera);
    composer.addPass(renderPass);

    outlinePass = new OutlinePass(
        new THREE.Vector2(container.clientWidth, container.clientWidth / aspect), 
        scene, 
        camera
    );
    // Adjusted settings
    outlinePass.edgeStrength = 2.0; // Reduced strength
    outlinePass.edgeGlow = 0.0; // Disabled glow
    outlinePass.edgeThickness = 0.8; // Reduced thickness
    outlinePass.pulsePeriod = 0;
    outlinePass.visibleEdgeColor.set('#ffff00');
    outlinePass.hiddenEdgeColor.set('#ffff00');
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
    document.getElementById('zoom-in')?.addEventListener('click', zoomIn);
    document.getElementById('zoom-out')?.addEventListener('click', zoomOut);
    document.getElementById('rotate-left')?.addEventListener('click', () => setRotation(-1));
    document.getElementById('rotate-right')?.addEventListener('click', () => setRotation(1));
    document.getElementById('pause-rotation')?.addEventListener('click', pauseRotation);
                 
     // Add event listeners for Environment controls
     document.getElementById('lighting-decrease-btn')?.addEventListener('click', decreaseLighting);
    document.getElementById('lighting-increase-btn')?.addEventListener('click', increaseLighting);
    document.getElementById('background-color')?.addEventListener('input', changeBackgroundColor);

    // Add click listener for object identification and selection
    renderer.domElement.addEventListener('click', onModelClick);

    // Add listener for the selected object color picker
    document.getElementById('selected-object-color-picker')?.addEventListener('input', onSelectedColorChange);
    
    // Add listener for the visibility toggle button
    document.getElementById('toggle-object-visibility')?.addEventListener('click', onToggleVisibilityClick);
    
    // Setup the right menu container for model groups (will be populated later)
    setupModelGroupsContainer();
    
     // Add window resize listener
     window.addEventListener('resize', onWindowResize);
     onWindowResize(); // Call once initially to set size
     
     // Add listener for fullscreen button
     document.getElementById('fullscreen-btn')?.addEventListener('click', toggleFullscreen);

     // Add listener for fullscreen change events (browser prefix handling)
     document.addEventListener('fullscreenchange', handleFullscreenChange);
     document.addEventListener('webkitfullscreenchange', handleFullscreenChange);
     document.addEventListener('mozfullscreenchange', handleFullscreenChange);
     document.addEventListener('MSFullscreenChange', handleFullscreenChange);
     
     // Add keyboard listener for ESC key to deselect objects
     document.addEventListener('keydown', handleKeyPress);
     
     // Add listener for right controls menu collapse button
     document.getElementById('right-menu-collapse-btn')?.addEventListener('click', () => {
         const menu = document.getElementById('right-controls-menu');
         const btn = document.getElementById('right-menu-collapse-btn');
         if (!menu || !btn) return;
         
         const isCollapsed = menu.dataset.collapsed === 'true';
         const menuHeight = menu.scrollHeight; // Get the full potential height

         if (isCollapsed) {
             // Expand: Slide back from left
             menu.style.transform = 'translateX(0)';
              menu.dataset.collapsed = 'false';
             btn.innerHTML = '&minus;';
         } else {
             // Collapse: Slide to the left
             const menuWidth = menu.offsetWidth;
             const hiddenWidth = Math.max(0, menuWidth - 30);
             menu.style.transform = `translateX(-${hiddenWidth}px)`; // Negative value for left slide
               menu.dataset.collapsed = 'true';
             btn.innerHTML = '&plus;';
         }
     });

    // Add listeners for panel switcher buttons
    document.getElementById('show-objects-library-btn')?.addEventListener('click', () => switchRightPanel('objects-library'));
    document.getElementById('show-model-groups-btn')?.addEventListener('click', () => switchRightPanel('model-groups'));
    document.getElementById('show-control-settings-btn')?.addEventListener('click', () => switchRightPanel('control-settings'));
    document.getElementById('show-rooms-btn')?.addEventListener('click', () => switchRightPanel('show-rooms'));
    
    // Initialize the Objects Library
    populateObjectsLibrary();
    
    // --- Room Visibility Functions ---
    populateRoomToggles();
    // --- End Room Visibility Functions ---

    // Initialize object tools only - remove non-existent function calls
    // initMenus();
    // initLoadButton(); 
    // initSliceControls();
    initObjectTools(); // Initialize object manipulation tools
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
    // RESTORE composer rendering
    composer.render(); 
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
        Object.keys(mtlMaterials.materials).forEach(materialName => {
             const currentMaterial = mtlMaterials.materials[materialName];
             if (!currentMaterial) return; // Skip if material doesn't exist

             // Enable shadows
             currentMaterial.receiveShadow = true; 
             currentMaterial.castShadow = true; 

             // REMOVED: Logic to set main color pickers based on `materials` object

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
             }
             // Setup default floor texture
             else if (materialName === 'interior_floor') {
                 currentMaterial.shininess = 30;
                 currentMaterial.specular = new THREE.Color(0x222222); 
                 applyTextureToMaterial(currentMaterial, 'wood'); // Apply default texture
                 // Ensure floor is opaque and writes to depth buffer
                 currentMaterial.transparent = false;
                 currentMaterial.depthWrite = true;
                 currentMaterial.depthTest = true;
             }
             else {
                 // For all other materials, ensure they are opaque and write depth
                 currentMaterial.transparent = false;
                 currentMaterial.depthWrite = true;
                 currentMaterial.depthTest = true;
                 currentMaterial.side = THREE.FrontSide;
             }
        }); // End loop

           objLoader.setMaterials(mtlMaterials);
           console.log(`Loading OBJ: ${objPath}`);
           objLoader.load(objPath, function(object) {
               console.log("OBJ loaded:", object);
               
               // Setup the loaded model (centralize all setup here)
               setupLoadedModel(object, objPath.split('/').pop());

           }, undefined, (error) => {
                console.error("Error loading OBJ file:", error);
           });
     }, undefined, (error) => {
         console.error("Error loading MTL file:", error);
         // Optionally, try loading OBJ without MTL
         // objLoader.load(objPath, function(object) { ... });
     });
}

function zoomIn() {
    if (!controls) return;
    // Get direction vector from camera to target
    const offset = new THREE.Vector3().subVectors(camera.position, controls.target);
    // Scale the offset vector (e.g., by 0.9 to zoom in)
    offset.multiplyScalar(0.9);
    // Calculate new position and move camera
    const newPosition = new THREE.Vector3().addVectors(controls.target, offset);
    camera.position.copy(newPosition);
    controls.update();
}

function zoomOut() {
    if (!controls) return;
    // Get direction vector from camera to target
    const offset = new THREE.Vector3().subVectors(camera.position, controls.target);
    // Scale the offset vector (e.g., by 1.1 to zoom out)
    offset.multiplyScalar(1.1);
    // Calculate new position and move camera
    const newPosition = new THREE.Vector3().addVectors(controls.target, offset);
    camera.position.copy(newPosition);
    controls.update();
}

// Function to decrease lighting intensity
function decreaseLighting() {
    let newMultiplier = Math.max(minLightIntensity, currentLightMultiplier - lightIntensityStep);
    updateAllLights(newMultiplier);
}

// Function to increase lighting intensity
function increaseLighting() {
    let newMultiplier = Math.min(maxLightIntensity, currentLightMultiplier + lightIntensityStep);
    updateAllLights(newMultiplier);
}

// Helper function to update all lights based on a multiplier
function updateAllLights(multiplier) {
    currentLightMultiplier = multiplier; // Store the new multiplier
    allLights.forEach(light => {
        if (initialIntensities[light.uuid] !== undefined) {
            light.intensity = initialIntensities[light.uuid] * currentLightMultiplier;
        }
    });
    console.log(`Lighting multiplier set to: ${currentLightMultiplier.toFixed(2)}`);
}

// Function to change background color
function changeBackgroundColor(event) {
    const color = new THREE.Color(event.target.value);
    scene.background = color;
}

// Event handler for object selection
function onModelClick(event) {
    const displayElement = document.getElementById('clicked-object-display');
    
    // Calculate mouse position in normalized device coordinates (-1 to +1) for component
    const rect = renderer.domElement.getBoundingClientRect();
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);

    // First clear any existing selection
    clearSelection();

    // Check for intersections with ALL objects in the scene, not just currentModel
    let intersects = [];
    
    // Get all selectable objects in the scene
    const selectableObjects = getSelectableObjects();
    if (selectableObjects.length > 0) {
        intersects = raycaster.intersectObjects(selectableObjects, false);
    }

    if (intersects.length > 0) {
        const intersection = intersects[0];
        const object = intersection.object; // The intersected mesh
        
        if (object instanceof THREE.Mesh) {
            selectObjectFromMenu(object); // Use the common selection function
        } else {
             // Might have clicked a line or point
             if(displayElement) displayElement.textContent = `Clicked: (Not a mesh - ${object.type})`;
        }
    }
}

// Helper function to get all selectable objects in the scene
function getSelectableObjects() {
    const objects = [];
    
    // Add the currentModel objects if available
    if (currentModel) {
        currentModel.traverse(child => {
            if (child instanceof THREE.Mesh) {
                objects.push(child);
            }
        });
    }
    
    // Add other objects added to the scene (e.g., from the Objects Library)
    scene.traverse(child => {
        // Only include meshes that aren't part of currentModel
        if (child instanceof THREE.Mesh && (!currentModel || !isChildOf(child, currentModel))) {
            objects.push(child);
        }
    });
    
    return objects;
}

// Helper function to check if an object is a child of another object
function isChildOf(child, parent) {
    let current = child.parent;
    while (current) {
        if (current === parent) {
            return true;
        }
        current = current.parent;
    }
    return false;
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
       
       // Scroll the content area of the right menu
       const menuContainer = document.getElementById('right-menu-content-area'); 
       if (foundItem) {
            // Calculate offset relative to the scrollable container
            const containerRect = menuContainer.getBoundingClientRect();
            const itemRect = foundItem.getBoundingClientRect();
            const offset = itemRect.top - containerRect.top + menuContainer.scrollTop;
            menuContainer.scrollTo({ top: offset, behavior: 'smooth' });
       }
  }


 // Handler for color change from the selected object picker
 function onSelectedColorChange(event) {
     if (selectedMaterialForEditing && selectedMeshForEditing) {
         const newColor = new THREE.Color(event.target.value);
         selectedMaterialForEditing.color.set(newColor);
         // Texture map is intentionally NOT removed here
         selectedMaterialForEditing.needsUpdate = true;
         console.log(`Set selected material color to ${event.target.value}`);
         
         // Update the corresponding color picker in the side menu 
         const sideMenuColorPicker = document.getElementById(`groupsContainer-color-${selectedMeshForEditing.uuid}`);
         if (sideMenuColorPicker) {
             sideMenuColorPicker.value = event.target.value;
         }
         // REMOVED: Texture dropdown reset logic
     } else {
          console.warn("Color changed but no material selected.");
     }
 }

 // Handler for visibility toggle button
 function onToggleVisibilityClick() {
     if (selectedMeshForEditing) {
         selectedMeshForEditing.visible = !selectedMeshForEditing.visible;
         const visibilityButton = document.getElementById('toggle-object-visibility');
         if(visibilityButton) visibilityButton.textContent = selectedMeshForEditing.visible ? 'Hide' : 'Show';
         console.log(`Toggled visibility for ${getHierarchicalName(selectedMeshForEditing)}. Now visible: ${selectedMeshForEditing.visible}`);
         
         // Update the corresponding visibility button in the side menu 
         const sideMenuVisBtn = document.getElementById(`groupsContainer-vis-${selectedMeshForEditing.uuid}`);
         if (sideMenuVisBtn) {
              sideMenuVisBtn.textContent = selectedMeshForEditing.visible ? 'Hide' : 'Show';
              // Update item opacity
              const sideMenuItem = sideMenuVisBtn.closest('.model-group-item');
              if (sideMenuItem) sideMenuItem.style.opacity = selectedMeshForEditing.visible ? '1' : '0.5';
         }
     } else {
         console.warn("Toggle visibility clicked, but no mesh selected.");
     }
 }

 // Setup the container where model groups will be listed in the right menu
 function setupModelGroupsContainer() {
     // This function now just ensures the target div exists.
     // The menu structure is already in the HTML.
     // Populate if model already loaded
     if (currentModel) {
         populateModelGroupsMenu();
     }
 }
 
 // NEW: Function to create UI controls for a single object (now only for side menu)
 // *Note*: targetContainer will now be #right-menu-model-groups-content
 function createObjectControlsUI(node, name, targetContainer) {
     const itemContainer = document.createElement('div');
     // Only side menu styling now
     itemContainer.className = 'model-group-item'; 
     itemContainer.style.opacity = node.visible ? '1' : '0.5';

     const header = document.createElement('div');
     header.className = 'model-group-header';
     const icon = document.createElement('div');
     icon.className = 'model-group-icon';
     icon.innerHTML = '&#9632;';
     header.appendChild(icon);

     const nameDisplay = document.createElement('div');
     nameDisplay.className = 'model-group-name';
     nameDisplay.textContent = name;
     nameDisplay.title = name;
     header.appendChild(nameDisplay);

     // Click selects object
     header.addEventListener('click', () => selectObjectFromMenu(node));
     itemContainer.appendChild(header);

     const controlsDiv = document.createElement('div');
     controlsDiv.className = 'model-group-controls';

     // Color Picker
     const colorPicker = document.createElement('input');
     colorPicker.type = 'color';
     const colorPickerId = `${targetContainer.id}-color-${node.uuid}`; // Unique ID
     colorPicker.id = colorPickerId;
     colorPicker.value = '#ffffff';
     const primaryMaterial = Array.isArray(node.material) ? node.material[0] : node.material;
     if (primaryMaterial && primaryMaterial.color) {
         colorPicker.value = '#' + primaryMaterial.color.getHexString();
     }
     colorPicker.style.width = '100%'; // Side menu style

     colorPicker.addEventListener('input', (e) => {
         const color = new THREE.Color(e.target.value);
         const materialsToUpdate = Array.isArray(node.material) ? node.material : [node.material];
         materialsToUpdate.forEach(mat => {
             if (mat) {
                 mat.color.set(color);
                 // Texture map is intentionally NOT removed here
                 mat.needsUpdate = true;
             }
         });
         // Update main interaction area if this is selected
         if (selectedMeshForEditing === node) {
             const interactionColorPicker = document.getElementById('selected-object-color-picker');
             if (interactionColorPicker) interactionColorPicker.value = e.target.value;
         }
         // REMOVED: Texture dropdown reset logic
     });
     controlsDiv.appendChild(colorPicker);

     // Texture Selector (only for floor objects)
     if (name.toLowerCase().includes('floor')) {
         const textureLabel = document.createElement('label');
         const textureSelectId = `${targetContainer.id}-texture-${node.uuid}`;
         textureLabel.textContent = 'Texture:';
         textureLabel.setAttribute('for', textureSelectId);
         textureLabel.style.cssText = 'display:block; margin-bottom:3px; font-size:12px; color:rgba(200,200,200,1);'; // Side menu style

         const textureSelect = document.createElement('select');
         textureSelect.id = textureSelectId;
         
         // Add "None" option
         textureSelect.add(new Option('None', ''));
         
         // Add all available flooring textures from the dynamic list
         flooringTextures.forEach(texture => {
             textureSelect.add(new Option(texture.text, texture.value));
         });

         // Set initial texture value based on current material map
         let initialTextureValue = '';
         if (primaryMaterial && primaryMaterial.map && primaryMaterial.map.image) {
             const currentTextureSrc = primaryMaterial.map.image.src;
             // Find matching texture by comparing image paths
             for (const texture of flooringTextures) {
                 if (currentTextureSrc.includes(texture.fileName)) {
                     initialTextureValue = texture.value;
                     break;
                 }
             }
         }
         textureSelect.value = initialTextureValue;

         textureSelect.style.width = '100%'; // Side menu style
         textureSelect.style.backgroundColor = '#555';
         textureSelect.style.color = 'white';
         textureSelect.style.border = '1px solid #777';
         textureSelect.style.borderRadius = '3px';
         textureSelect.style.padding = '4px';
         textureSelect.style.fontSize = '12px';

         textureSelect.addEventListener('change', (e) => {
             const textureType = e.target.value;
             const materialsToUpdate = Array.isArray(node.material) ? node.material : [node.material];
             materialsToUpdate.forEach(mat => {
                 if (mat) {
                     if (textureType) {
                         applyTextureToMaterial(mat, textureType);
                     } else {
                         mat.map = null;
                         mat.needsUpdate = true;
                     }
                 }
             });
         });
         controlsDiv.appendChild(textureLabel);
         controlsDiv.appendChild(textureSelect);
     }

     // Visibility Toggle Button
     const visibilityBtn = document.createElement('button');
     const visibilityBtnId = `${targetContainer.id}-vis-${node.uuid}`; // Unique ID
     visibilityBtn.id = visibilityBtnId;
     visibilityBtn.textContent = node.visible ? 'Hide' : 'Show';
     visibilityBtn.style.cssText = 'width:100%; padding:4px; margin-top:5px; background-color:#555; color:white; border:1px solid #777; border-radius:3px; cursor:pointer; font-size:12px;'; // Side menu style
     
     visibilityBtn.addEventListener('click', () => {
         node.visible = !node.visible;
         visibilityBtn.textContent = node.visible ? 'Hide' : 'Show';
         itemContainer.style.opacity = node.visible ? '1' : '0.5';
         // Update main interaction area if this is selected
         if (selectedMeshForEditing === node) {
             const interactionVisBtn = document.getElementById('toggle-object-visibility');
             if (interactionVisBtn) interactionVisBtn.textContent = node.visible ? 'Hide' : 'Show';
         }
     });
     // Add hover effect only for side menu button
     visibilityBtn.onmouseover = () => { visibilityBtn.style.backgroundColor = '#666'; };
     visibilityBtn.onmouseout = () => { visibilityBtn.style.backgroundColor = '#555'; };
     controlsDiv.appendChild(visibilityBtn);

     itemContainer.appendChild(controlsDiv);
     targetContainer.appendChild(itemContainer);
 }

 // Function to populate the model groups menu
 function populateModelGroupsMenu() {
     // Target the new container within the right menu
     const groupsContainer = document.getElementById('right-menu-model-groups-content');
      // REMOVED: Reference to mainControlsContainer
      if (!groupsContainer) {
           console.error("Required container element 'right-menu-model-groups-content' not found.");
           return;
      }

     groupsContainer.innerHTML = ''; // Clear existing side menu entries
      // REMOVED: Clearing mainControlsContainer

     if (!currentModel) return;

     const groupsMap = new Map();

     // Traverse to find all unique meshes
      currentModel.traverse((node) => {
          if (node instanceof THREE.Mesh) {
              const hierarchicalName = getHierarchicalName(node);
              if (!groupsMap.has(hierarchicalName)) {
                  groupsMap.set(hierarchicalName, node);
              }
          }
      });

     // Sort groups alphabetically by name
     const sortedGroups = Array.from(groupsMap.entries()).sort((a, b) => a[0].localeCompare(b[0]));

     // Create UI elements for each group ONLY in the side menu
     sortedGroups.forEach(([name, node]) => {
          // Only call for the side menu container
          createObjectControlsUI(node, name, groupsContainer);
          // REMOVED: Call to populate main controls area
     });

     // Message if no groups found
     if (sortedGroups.length === 0) {
         const noGroupsMsg = document.createElement('p');
         noGroupsMsg.textContent = 'No distinct objects found in model.';
         noGroupsMsg.style.fontStyle = 'italic';
         noGroupsMsg.style.padding = '10px';
         noGroupsMsg.style.textAlign = 'center';
         groupsContainer.appendChild(noGroupsMsg); // Add only to side menu
         // REMOVED: Adding message to main controls container
     }
 }
 
 // Function to programmatically select an object (e.g., when clicked in the menu)
 function selectObjectFromMenu(node) {
      if (!(node instanceof THREE.Mesh)) return;

      // Reset previous selection visuals ONLY in side menu
      document.querySelectorAll('#right-menu-model-groups-content .model-group-item').forEach(item => { 
          item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)';
          // Reset text color
          const nameEl = item.querySelector('.model-group-name');
          if (nameEl) nameEl.style.color = '#eee'; // Default/reset color
      });
      // REMOVED: Querying/resetting .material-control items

      // Set new selection
      // Reset previous highlight (OutlinePass handles this implicitly)
      selectedMeshForEditing = node;
      outlinePass.selectedObjects = [node]; // Use OutlinePass again

      // Determine material (use primary if multi-material)
      const primaryMaterial = Array.isArray(node.material) ? node.material[0] : node.material;
      selectedMaterialForEditing = primaryMaterial || null;

      const objectName = getHierarchicalName(node);

      // Update main interaction area display (still needed)
      const displayElement = document.querySelector('#right-menu-control-settings-content #clicked-object-display');
      const colorPicker = document.getElementById('selected-object-color-picker');
      const visibilityButton = document.getElementById('toggle-object-visibility');

      if(displayElement) displayElement.textContent = `Selected: ${objectName}`;

      if (selectedMaterialForEditing) {
          if(colorPicker) {
              colorPicker.value = '#' + selectedMaterialForEditing.color.getHexString();
              colorPicker.style.display = 'inline-block';
          }
      } else {
          if(colorPicker) colorPicker.style.display = 'none';
      }

      if(visibilityButton) {
         visibilityButton.textContent = node.visible ? 'Hide' : 'Show';
         visibilityButton.style.display = 'inline-block';
      }

      // Highlight the item ONLY in the side menu (now the right menu)
      // Ensure ID prefix matches the new target container ID ('right-menu-model-groups-content')
      const menuItem = document.getElementById(`right-menu-model-groups-content-color-${node.uuid}`)?.closest('.model-group-item');
      if (menuItem) {
           menuItem.style.backgroundColor = 'rgba(80, 80, 80, 0.9)'; // Highlight color
           // Highlight text color
           const nameEl = menuItem.querySelector('.model-group-name');
           if (nameEl) nameEl.style.color = 'yellow';
           
           // Scroll the content area of the right menu
           const menuContainer = document.getElementById('right-menu-content-area');
           if (menuContainer) {
                // Calculate offset relative to the scrollable container
                const containerRect = menuContainer.getBoundingClientRect();
                const itemRect = menuItem.getBoundingClientRect();
                const offset = itemRect.top - containerRect.top + menuContainer.scrollTop;
                menuContainer.scrollTo({ top: offset, behavior: 'smooth' });
           }
      }
      // REMOVED: Highlighting/scrolling in the removed main controls area
      
      // Only show the object toolbar if the object was added from the objects library
      // Objects added from the library have names that start with "placed_"
      if (node.name && node.name.startsWith("placed_")) {
          showObjectToolbar();
      } else {
          hideObjectToolbar();
      }
 }
 
  // Handle window resize AND fullscreen changes
 function onWindowResize() {
     const container = document.getElementById('threejs-viewer');
     if (!container) return;
     
     const isFullscreen = document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement;
     let newWidth, newHeight;

     if (isFullscreen) {
         // Use full window dimensions when fullscreen
         newWidth = window.innerWidth;
         newHeight = window.innerHeight;
     } else {
         // Use container dimensions when not fullscreen
         newWidth = container.clientWidth;
         // Calculate height based on aspect ratio, respecting container max-height
         const aspect = 16 / 12; 
         newHeight = Math.min(container.clientHeight, newWidth / aspect);
         // If flex container squishes it, use clientHeight
         if (container.clientHeight > 0 && newHeight > container.clientHeight) {
             newHeight = container.clientHeight;
             newWidth = newHeight * aspect; // Adjust width to maintain aspect if height is limited
         }
     }

     // Update camera aspect ratio
     camera.aspect = newWidth / newHeight;
     camera.updateProjectionMatrix();

     // Update renderer size
     renderer.setSize(newWidth, newHeight);
     // RESTORE composer and outlinePass resize
     composer.setSize(newWidth, newHeight);
     outlinePass.resolution.set(newWidth, newHeight);

     console.log(`Resized to: ${newWidth}x${newHeight}, Fullscreen: ${!!isFullscreen}`);
 }
 
 // Toggle Fullscreen Function
 function toggleFullscreen() {
     const viewerElement = document.getElementById('threejs-viewer');
     if (!viewerElement) return;
     
     if (!document.fullscreenElement && !document.webkitFullscreenElement && !document.mozFullScreenElement && !document.msFullscreenElement) {
         // Enter fullscreen
         if (viewerElement.requestFullscreen) {
             viewerElement.requestFullscreen();
         } else if (viewerElement.webkitRequestFullscreen) { /* Safari */
             viewerElement.webkitRequestFullscreen();
         } else if (viewerElement.mozRequestFullScreen) { /* Firefox */
             viewerElement.mozRequestFullScreen();
         } else if (viewerElement.msRequestFullscreen) { /* IE11 */
             viewerElement.msRequestFullscreen();
         }
     } else {
         // Exit fullscreen
         if (document.exitFullscreen) {
             document.exitFullscreen();
         } else if (document.webkitExitFullscreen) { /* Safari */
             document.webkitExitFullscreen();
         } else if (document.mozCancelFullScreen) { /* Firefox */
             document.mozCancelFullScreen();
         } else if (document.msExitFullscreen) { /* IE11 */
             document.msExitFullscreen();
         }
     }
 }
 
 // Function to update button icon based on fullscreen state
 function handleFullscreenChange() {
     const fullscreenBtnIcon = document.querySelector('#fullscreen-btn i');
     if (!fullscreenBtnIcon) return;

     if (document.fullscreenElement || document.webkitFullscreenElement || document.mozFullScreenElement || document.msFullscreenElement) {
         fullscreenBtnIcon.classList.remove('fa-expand');
         fullscreenBtnIcon.classList.add('fa-compress');
     } else {
         // Not fullscreen: Show expand icon
         fullscreenBtnIcon.classList.remove('fa-compress');
         fullscreenBtnIcon.classList.add('fa-expand'); // Use correct variable
     }
     // Trigger resize explicitly after fullscreen change
     setTimeout(onWindowResize, 50); // Small delay often helps rendering
 }
 
 // Function to switch panels in the RIGHT menu
 function switchRightPanel(panelToShow) {
     const objectsLibraryPanel = document.getElementById('right-menu-objects-library-content');
     const modelGroupsPanel = document.getElementById('right-menu-model-groups-content');
     const controlSettingsPanel = document.getElementById('right-menu-control-settings-content');
     const showRoomsPanel = document.getElementById('right-menu-show-rooms-content'); // New panel
     const objectsLibraryBtn = document.getElementById('show-objects-library-btn');
     const modelGroupsBtn = document.getElementById('show-model-groups-btn');
     const controlSettingsBtn = document.getElementById('show-control-settings-btn');
     const showRoomsBtn = document.getElementById('show-rooms-btn'); // New button
     
     if (!objectsLibraryPanel || !modelGroupsPanel || !controlSettingsPanel || !showRoomsPanel || 
         !objectsLibraryBtn || !modelGroupsBtn || !controlSettingsBtn || !showRoomsBtn) {
         console.error("One or more right menu panels/buttons not found");
         return;
     }
     
     // Hide all panels first
     objectsLibraryPanel.style.display = 'none';
     modelGroupsPanel.style.display = 'none';
     controlSettingsPanel.style.display = 'none';
     showRoomsPanel.style.display = 'none';
     objectsLibraryBtn.classList.remove('active');
     modelGroupsBtn.classList.remove('active');
     controlSettingsBtn.classList.remove('active');
     showRoomsBtn.classList.remove('active');
     
     if (panelToShow === 'objects-library') {
         objectsLibraryPanel.style.display = 'block';
         objectsLibraryBtn.classList.add('active');
     } else if (panelToShow === 'model-groups') {
         modelGroupsPanel.style.display = 'block';
         modelGroupsBtn.classList.add('active');
     } else if (panelToShow === 'control-settings') {
         controlSettingsPanel.style.display = 'block';
         controlSettingsBtn.classList.add('active');
     } else if (panelToShow === 'show-rooms') {
         showRoomsPanel.style.display = 'block';
         showRoomsBtn.classList.add('active');
     }
     // Ensure the content area can scroll if needed
     document.getElementById('right-menu-content-area')?.scrollTo(0, 0);
 }
 
 // --- Room Visibility Functions ---
 function populateRoomToggles() {
     const contentDiv = document.getElementById('right-menu-show-rooms-content');
     if (!contentDiv) return;

     // Clear existing toggles
     contentDiv.innerHTML = '';

     // Add 'All' toggle
     const allItemDiv = document.createElement('div');
     allItemDiv.className = 'room-toggle-item';

     const allCheckbox = document.createElement('input');
     allCheckbox.type = 'checkbox';
     allCheckbox.id = 'toggle-all-rooms';
     allCheckbox.checked = true;
     allCheckbox.addEventListener('change', handleRoomToggleChange);

     const allLabel = document.createElement('label');
     allLabel.htmlFor = 'toggle-all-rooms';
     allLabel.textContent = 'All';

     allItemDiv.appendChild(allCheckbox);
     allItemDiv.appendChild(allLabel);
     contentDiv.appendChild(allItemDiv);

     // Create toggles for discovered rooms with nested object toggles
     roomPrefixes.forEach(prefix => {
         // Check if map has the prefix AND the set is not empty
         if (roomMeshesMap.has(prefix) && roomMeshesMap.get(prefix).size > 0) {
             const roomObjects = Array.from(roomMeshesMap.get(prefix));
             
             // Main room toggle item
             const roomDiv = document.createElement('div');
             roomDiv.className = 'room-toggle-item';
             
             // Room checkbox
             const roomCheckbox = document.createElement('input');
             roomCheckbox.type = 'checkbox';
             roomCheckbox.id = `toggle-${prefix}`;
             roomCheckbox.dataset.roomPrefix = prefix;
             roomCheckbox.checked = true;
             roomCheckbox.addEventListener('change', e => {
                 // Update all child checkboxes
                 const objectsContainer = document.getElementById(`objects-${prefix}`);
                 if (objectsContainer) {
                     const childCheckboxes = objectsContainer.querySelectorAll('input[type="checkbox"]');
                     childCheckboxes.forEach(cb => cb.checked = e.target.checked);
                 }
                 
                 handleRoomToggleChange(e);
             });
             
             // Room label
             const roomLabel = document.createElement('label');
             roomLabel.htmlFor = `toggle-${prefix}`;
             roomLabel.textContent = prefix.replace(/_/g, ' ');
             
             // Dropdown toggle button (▶)
             const dropdownBtn = document.createElement('button');
             dropdownBtn.className = 'dropdown-toggle';
             dropdownBtn.innerHTML = '▶';
             dropdownBtn.addEventListener('click', () => {
                 const objectsContainer = document.getElementById(`objects-${prefix}`);
                 if (objectsContainer) {
                     const isVisible = objectsContainer.classList.toggle('visible');
                     dropdownBtn.classList.toggle('expanded', isVisible);
                 }
             });
             
             // Add room toggle elements
             roomDiv.appendChild(roomCheckbox);
             roomDiv.appendChild(roomLabel);
             roomDiv.appendChild(dropdownBtn);
             contentDiv.appendChild(roomDiv);
             
             // Create container for object toggles
             const objectsContainer = document.createElement('div');
             objectsContainer.className = 'room-objects-container';
             objectsContainer.id = `objects-${prefix}`;
             
             // Add individual object toggles
             roomObjects.forEach(obj => {
                 const objDiv = document.createElement('div');
                 objDiv.className = 'object-toggle-item';
                 
                 const objCheckbox = document.createElement('input');
                 objCheckbox.type = 'checkbox';
                 objCheckbox.id = `toggle-object-${obj.uuid}`;
                 objCheckbox.dataset.objectId = obj.uuid;
                 objCheckbox.dataset.roomPrefix = prefix;
                 objCheckbox.checked = true;
                 objCheckbox.addEventListener('change', e => {
                     // Update object visibility directly
                     obj.visible = e.target.checked;
                     
                     // Update room checkbox if needed
                     updateRoomCheckboxState(prefix);
                     
                     // Update "All" checkbox
                     updateAllCheckboxState();
                 });
                 
                 const objLabel = document.createElement('label');
                 objLabel.htmlFor = `toggle-object-${obj.uuid}`;
                 objLabel.textContent = getObjectDisplayName(obj, prefix);
                 objLabel.title = obj.name; // Add full name as title for tooltip
                 
                 objDiv.appendChild(objCheckbox);
                 objDiv.appendChild(objLabel);
                 objectsContainer.appendChild(objDiv);
             });
             
             contentDiv.appendChild(objectsContainer);
         }
     });
     
     // Add Misc category with all unmatched objects
     if (roomMeshesMap.has(MISC_CATEGORY) && roomMeshesMap.get(MISC_CATEGORY).size > 0) {
         const miscObjects = Array.from(roomMeshesMap.get(MISC_CATEGORY));
         
         // Main misc toggle
         const miscDiv = document.createElement('div');
         miscDiv.className = 'room-toggle-item';
         
         const miscCheckbox = document.createElement('input');
         miscCheckbox.type = 'checkbox';
         miscCheckbox.id = `toggle-${MISC_CATEGORY}`;
         miscCheckbox.dataset.roomPrefix = MISC_CATEGORY;
         miscCheckbox.checked = true;
         miscCheckbox.addEventListener('change', e => {
             // Update all child checkboxes
             const objectsContainer = document.getElementById(`objects-${MISC_CATEGORY}`);
             if (objectsContainer) {
                 const childCheckboxes = objectsContainer.querySelectorAll('input[type="checkbox"]');
                 childCheckboxes.forEach(cb => cb.checked = e.target.checked);
             }
             
             handleRoomToggleChange(e);
         });
         
         const miscLabel = document.createElement('label');
         miscLabel.htmlFor = `toggle-${MISC_CATEGORY}`;
         miscLabel.textContent = MISC_CATEGORY;
         
         // Dropdown toggle
         const dropdownBtn = document.createElement('button');
         dropdownBtn.className = 'dropdown-toggle';
         dropdownBtn.innerHTML = '▶';
         dropdownBtn.addEventListener('click', () => {
             const objectsContainer = document.getElementById(`objects-${MISC_CATEGORY}`);
             if (objectsContainer) {
                 const isVisible = objectsContainer.classList.toggle('visible');
                 dropdownBtn.classList.toggle('expanded', isVisible);
             }
         });
         
         miscDiv.appendChild(miscCheckbox);
         miscDiv.appendChild(miscLabel);
         miscDiv.appendChild(dropdownBtn);
         contentDiv.appendChild(miscDiv);
         
         // Container for misc objects
         const miscObjectsContainer = document.createElement('div');
         miscObjectsContainer.className = 'room-objects-container';
         miscObjectsContainer.id = `objects-${MISC_CATEGORY}`;
         
         // Add individual misc object toggles
         miscObjects.forEach(obj => {
             const objDiv = document.createElement('div');
             objDiv.className = 'object-toggle-item';
             
             const objCheckbox = document.createElement('input');
             objCheckbox.type = 'checkbox';
             objCheckbox.id = `toggle-object-${obj.uuid}`;
             objCheckbox.dataset.objectId = obj.uuid;
             objCheckbox.dataset.roomPrefix = MISC_CATEGORY;
             objCheckbox.checked = true;
             objCheckbox.addEventListener('change', e => {
                 // Update object visibility directly
                 obj.visible = e.target.checked;
                 
                 // Update misc checkbox if needed
                 updateRoomCheckboxState(MISC_CATEGORY);
                 
                 // Update "All" checkbox
                 updateAllCheckboxState();
             });
             
             const objLabel = document.createElement('label');
             objLabel.htmlFor = `toggle-object-${obj.uuid}`;
             objLabel.textContent = getObjectDisplayName(obj, MISC_CATEGORY);
             objLabel.title = obj.name; // Add full name as title for tooltip
             
             objDiv.appendChild(objCheckbox);
             objDiv.appendChild(objLabel);
             miscObjectsContainer.appendChild(objDiv);
         });
         
         contentDiv.appendChild(miscObjectsContainer);
     }
 }

 // Helper function to get a more user-friendly object name
 function getObjectDisplayName(obj, category) {
     if (!obj || !obj.name) return 'Unnamed';
     
     // For Misc category, show the full name
     if (category === MISC_CATEGORY) {
         return obj.name;
     }
     
     // Remove any prefix paths like "path/to/model/"
     let name = obj.name.split('/').pop();
     
     // Show only the last part after underscore if it has one
     if (name.includes('_')) {
         const parts = name.split('_');
         if (parts.length > 1) {
             // Return last part, keeping the part after the last underscore
             return parts[parts.length-1];
         }
     }
     
     return name;
 }

 // Helper function to update a room checkbox based on its object checkboxes
 function updateRoomCheckboxState(prefix) {
     const roomCheckbox = document.getElementById(`toggle-${prefix}`);
     const objectsContainer = document.getElementById(`objects-${prefix}`);
     
     if (roomCheckbox && objectsContainer) {
         const childCheckboxes = objectsContainer.querySelectorAll('input[type="checkbox"]');
         if (childCheckboxes.length === 0) return;
         
         const allChecked = Array.from(childCheckboxes).every(cb => cb.checked);
         const anyChecked = Array.from(childCheckboxes).some(cb => cb.checked);
         
         // Set the checkbox state based on child checkboxes
         roomCheckbox.checked = anyChecked;
         
         // In the future, could use indeterminate state when some are checked
         // roomCheckbox.indeterminate = anyChecked && !allChecked;
     }
 }

 // Helper function to update the "All" checkbox state
 function updateAllCheckboxState() {
     const allCheckbox = document.getElementById('toggle-all-rooms');
     if (!allCheckbox) return;
     
     const roomCheckboxes = document.querySelectorAll(
         '.room-toggle-item > input[type="checkbox"]:not(#toggle-all-rooms)'
     );
     
     if (roomCheckboxes.length === 0) return;
     
     const allChecked = Array.from(roomCheckboxes).every(cb => cb.checked);
     const anyChecked = Array.from(roomCheckboxes).some(cb => cb.checked);
     
     // Set the "All" checkbox state
     allCheckbox.checked = anyChecked;
     
     // In the future, could use indeterminate state when some are checked
     // allCheckbox.indeterminate = anyChecked && !allChecked;
 }

 function handleRoomToggleChange(event) {
     const targetId = event.target.id;
     const isChecked = event.target.checked;

     if (targetId === 'toggle-all-rooms') {
         // Toggle all room checkboxes
         document.querySelectorAll('.room-toggle-item > input[type="checkbox"]:not(#toggle-all-rooms)').forEach(cb => {
             cb.checked = isChecked;
             
             // Also update object checkboxes within each room
             const prefix = cb.dataset.roomPrefix;
             if (prefix) {
                 const objectsContainer = document.getElementById(`objects-${prefix}`);
                 if (objectsContainer) {
                     objectsContainer.querySelectorAll('input[type="checkbox"]').forEach(objCb => {
                         objCb.checked = isChecked;
                     });
                 }
             }
         });
         
         // Update all object visibilities
         updateAllObjectVisibilities();
     } else {
         // A room checkbox was clicked
         const prefix = event.target.dataset.roomPrefix;
         if (prefix) {
             // Update "All" checkbox based on all room checkboxes
             updateAllCheckboxState();
             
             // Update visibility directly without using updateRoomVisibility
             // since we're now controlling visibility at the object level
             updateVisibilityForRoom(prefix);
         }
     }
 }

 // Update visibility for all objects in a specific room
 function updateVisibilityForRoom(prefix) {
     if (!roomMeshesMap.has(prefix)) return;
     
     const roomCheckbox = document.getElementById(`toggle-${prefix}`);
     if (!roomCheckbox) return;
     
     const isVisible = roomCheckbox.checked;
     
     // Get all object checkboxes for this room
     const objectsContainer = document.getElementById(`objects-${prefix}`);
     if (objectsContainer) {
         const objectCheckboxes = objectsContainer.querySelectorAll('input[type="checkbox"]');
         
         // For each object in this room
         roomMeshesMap.get(prefix).forEach(mesh => {
             if (mesh) {
                 // Find the corresponding checkbox
                 const checkbox = document.getElementById(`toggle-object-${mesh.uuid}`);
                 // Set visibility based on checkbox (or room checkbox if no specific object checkbox)
                 mesh.visible = checkbox ? checkbox.checked : isVisible;
             }
         });
     } else {
         // Fallback: set visibility based on room checkbox
         roomMeshesMap.get(prefix).forEach(mesh => {
             if (mesh) mesh.visible = isVisible;
         });
     }
     
     // Update the model groups menu
     updateModelGroupsVisibility();
 }

 // Update visibility for all objects in all rooms
 function updateAllObjectVisibilities() {
     const allCategories = [...roomPrefixes, MISC_CATEGORY];
     allCategories.forEach(category => {
         updateVisibilityForRoom(category);
     });
 }

 // Update the model groups menu to reflect current visibility
 function updateModelGroupsVisibility() {
     if (currentModel) {
         currentModel.traverse(node => {
             if (node instanceof THREE.Mesh) {
                 const menuItem = document.getElementById(`right-menu-model-groups-content-vis-${node.uuid}`)?.closest('.model-group-item');
                 const visBtn = document.getElementById(`right-menu-model-groups-content-vis-${node.uuid}`);
                 
                 if (menuItem) {
                     menuItem.style.opacity = node.visible ? '1' : '0.5';
                 }
                 if (visBtn) {
                     visBtn.textContent = node.visible ? 'Hide' : 'Show';
                 }
             }
         });
     }
 }
 // --- End Room Visibility Functions ---

 // Helper function to set up the model once loaded
 function setupLoadedModel(object, modelName) {
     console.log(`Setting up model: ${modelName}`);

     // Map rooms only if it's the house model
     if (modelName === 'pk4.obj') {
         roomMeshesMap.clear();
         roomPrefixes.forEach(prefix => roomMeshesMap.set(prefix, new Set()));
         roomMeshesMap.set(MISC_CATEGORY, new Set()); // Add Misc category

         // First set all meshes to visible since "All" is checked by default
         object.traverse((node) => {
             if (node instanceof THREE.Mesh) {
                 node.visible = true;
             }
         });

         // Then map meshes to room prefixes 
         object.traverse((node) => {
             if (node instanceof THREE.Mesh && node.name) {
                 let matched = false;
                 for (const prefix of roomPrefixes) {
                     // Use startsWith for prefix matching
                     if (node.name.startsWith(prefix)) { 
                         roomMeshesMap.get(prefix)?.add(node); 
                         matched = true;
                         break; 
                     }
                 }
                 // If no room prefix matched, add to Misc category
                 if (!matched) {
                     roomMeshesMap.get(MISC_CATEGORY)?.add(node);
                 }
             }
         });
         console.log("Room meshes mapped:", roomMeshesMap);
         populateRoomToggles(); // Create the checkboxes
         
         // Switch to the Rooms tab to make it obvious to the user
         switchRightPanel('show-rooms');
     } else {
         // If another model is loaded, clear the map and toggles
         roomMeshesMap.clear();
         populateRoomToggles(); 
     }

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
 }

 // Handle keyboard events
 function handleKeyPress(event) {
     // Handle ESC key (key code 27)
     if (event.key === 'Escape' || event.keyCode === 27) {
         clearSelection();
     }
 }

 // Clear the current object selection
 function clearSelection() {
    // Reset previous selection visuals (OutlinePass)
    outlinePass.selectedObjects = []; 
    selectedMeshForEditing = null;
    selectedMaterialForEditing = null;
    
    // Update UI elements
    const displayElement = document.getElementById('clicked-object-display');
    const colorPicker = document.getElementById('selected-object-color-picker');
    const visibilityButton = document.getElementById('toggle-object-visibility');
    
    if(colorPicker) colorPicker.style.display = 'none';
    if(visibilityButton) visibilityButton.style.display = 'none';
    if(displayElement) displayElement.textContent = 'Clicked: (None)';
    
    // Reset model groups menu item highlights
    document.querySelectorAll('.model-group-item').forEach(item => {
        item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)'; // Reset menu item background
        // Reset text color as well
        const nameEl = item.querySelector('.model-group-name');
        if (nameEl) nameEl.style.color = '#eee'; // Default/reset color
    });
    
    // Always hide the object toolbar when selection is cleared
    hideObjectToolbar();
    
    // Reset transform state
    isTransforming = false;
    transformType = null;
    transformAxis = null;
    
    console.log('Selection cleared');
}

 // Function to populate the objects library with draggable items
 function populateObjectsLibrary() {
     const container = document.getElementById('right-menu-objects-library-content');
     if (!container) return;
     
     const objectsList = container.querySelector('.draggable-objects-list');
     if (!objectsList) return;
     
     // Clear existing items
     objectsList.innerHTML = '';
     
     // Create drop indicator element if it doesn't exist
     if (!dropIndicator) {
         dropIndicator = document.createElement('div');
         dropIndicator.className = 'drop-indicator';
         document.getElementById('threejs-viewer')?.appendChild(dropIndicator);
     }
     
     // Add each object as a draggable item
     availableObjects.forEach(obj => {
         const item = document.createElement('div');
         item.className = 'draggable-object-item';
         item.draggable = true;
         item.dataset.objectName = obj.name;
         item.dataset.objectType = obj.type;
         item.dataset.objectColor = obj.color;
         
         const iconDiv = document.createElement('div');
         iconDiv.className = 'draggable-object-icon';
         iconDiv.style.color = '#' + obj.color.toString(16).padStart(6, '0');
         
         // Use icon
         const icon = document.createElement('i');
         icon.className = obj.icon;
         iconDiv.appendChild(icon);
         
         const nameDiv = document.createElement('div');
         nameDiv.className = 'draggable-object-name';
         nameDiv.textContent = obj.name;
         
         item.appendChild(iconDiv);
         item.appendChild(nameDiv);
         
         // Add drag event listeners
         item.addEventListener('dragstart', handleDragStart);
         item.addEventListener('dragend', handleDragEnd);
         
         objectsList.appendChild(item);
     });
     
     // Add events to the viewer for drop functionality
     const viewer = document.getElementById('threejs-viewer');
     if (viewer) {
         viewer.addEventListener('dragover', handleDragOver);
         viewer.addEventListener('dragleave', handleDragLeave);
         viewer.addEventListener('drop', handleDrop);
     }
 }

 // Handle drag start
 function handleDragStart(event) {
     isDragging = true;
     draggedObject = event.target;
     
     // Add dragging class for visual feedback
     draggedObject.classList.add('dragging');
     
     // Set data transfer properties
     event.dataTransfer.setData('text/plain', draggedObject.dataset.objectName);
     event.dataTransfer.effectAllowed = 'copy';
     
     // For Firefox compatibility (needs to set data)
     if (event.dataTransfer.setDragImage) {
         const dragIcon = draggedObject.querySelector('.draggable-object-icon');
         if (dragIcon) {
             event.dataTransfer.setDragImage(dragIcon, 32, 32);
         }
     }
 }

 // Handle drag end
 function handleDragEnd(event) {
     isDragging = false;
     if (draggedObject) {
         draggedObject.classList.remove('dragging');
     }
     draggedObject = null;
     
     // Hide drop indicator
     if (dropIndicator) {
         dropIndicator.style.display = 'none';
     }
 }

 // Handle drag over viewer
 function handleDragOver(event) {
     // Prevent default to allow drop
     event.preventDefault();
     
     // Set drop effect
     event.dataTransfer.dropEffect = 'copy';
     
     // Show and position the drop indicator
     if (dropIndicator) {
         dropIndicator.style.display = 'block';
         dropIndicator.style.left = (event.clientX - 25) + 'px';
         dropIndicator.style.top = (event.clientY - 25) + 'px';
     }
 }

 // Handle drag leave
 function handleDragLeave(event) {
     // Hide drop indicator
     if (dropIndicator) {
         dropIndicator.style.display = 'none';
     }
 }

 // Handle drop
 function handleDrop(event) {
     // Prevent default browser behavior
     event.preventDefault();
     
     // Hide drop indicator
     if (dropIndicator) {
         dropIndicator.style.display = 'none';
     }
     
     // Get the dropped object name
     const objectName = event.dataTransfer.getData('text/plain');
     if (!objectName) return;
     
     // Get object details
     const objectData = availableObjects.find(obj => obj.name === objectName);
     if (!objectData) return;
     
     // Get drop position in 3D space
     const dropPosition = getDropPosition(event);
     
     // Create and place the object
     createAndPlaceShape(objectData, dropPosition);
 }

 // Function to create and place a 3D shape in the scene
 function createAndPlaceShape(objectData, position) {
     // Create geometry based on shape type
     let geometry;
     const name = objectData.name.toLowerCase();
     
     // Reduce size by 75% - make shapes much smaller
     const scaleFactor = 0.25; // 25% of original size
     
     switch (name) {
         case 'cube':
             geometry = new THREE.BoxGeometry(scaleFactor, scaleFactor, scaleFactor);
             break;
         case 'sphere':
             geometry = new THREE.SphereGeometry(0.5 * scaleFactor, 32, 32);
             break;
         case 'cylinder':
             geometry = new THREE.CylinderGeometry(0.5 * scaleFactor, 0.5 * scaleFactor, 1 * scaleFactor, 32);
             break;
         case 'cone':
             geometry = new THREE.ConeGeometry(0.5 * scaleFactor, 1 * scaleFactor, 32);
             break;
         case 'torus':
             geometry = new THREE.TorusGeometry(0.5 * scaleFactor, 0.2 * scaleFactor, 16, 32);
             break;
         case 'pyramid':
             geometry = new THREE.ConeGeometry(0.5 * scaleFactor, 1 * scaleFactor, 4);
             break;
         case 'trapezoid':
             // Create a custom trapezoid geometry
             geometry = createTrapezoidGeometry(1 * scaleFactor, 0.6 * scaleFactor, 0.5 * scaleFactor, 1 * scaleFactor);
             break;
         default:
             geometry = new THREE.BoxGeometry(scaleFactor, scaleFactor, scaleFactor);
             break;
     }
     
     // Create material with the color
     const material = new THREE.MeshStandardMaterial({
         color: objectData.color,
         metalness: 0.3,
         roughness: 0.6
     });
     
     // Create mesh
     const mesh = new THREE.Mesh(geometry, material);
     mesh.name = `placed_${name}_${Date.now()}`;
     
     // Enable shadows
     mesh.castShadow = true;
     mesh.receiveShadow = true;
     
     // Position the mesh
     mesh.position.copy(position);
     
     // Add to scene
     scene.add(mesh);
     
     // Add to the Misc category for room visibility
     if (roomMeshesMap.has(MISC_CATEGORY)) {
         roomMeshesMap.get(MISC_CATEGORY).add(mesh);
     }
     
     console.log(`Shape ${name} added to scene at position:`, position);
     
     // Update the model groups menu to include the new shape
     populateModelGroupsMenu();
     
     // Update room toggles to include the new object
     populateRoomToggles();
     
     // Select the newly added object
     selectObjectFromMenu(mesh);
 }

 // Custom function to create a trapezoid geometry
 function createTrapezoidGeometry(topWidth, bottomWidth, height, depth) {
     const geometry = new THREE.BufferGeometry();
     
     // Define the vertices
     const halfTopWidth = topWidth / 2;
     const halfBottomWidth = bottomWidth / 2;
     const halfHeight = height / 2;
     const halfDepth = depth / 2;
     
     const vertices = new Float32Array([
         // Top face
         -halfTopWidth, halfHeight, halfDepth,
         halfTopWidth, halfHeight, halfDepth,
         halfTopWidth, halfHeight, -halfDepth,
         -halfTopWidth, halfHeight, -halfDepth,
         
         // Bottom face
         -halfBottomWidth, -halfHeight, halfDepth,
         halfBottomWidth, -halfHeight, halfDepth,
         halfBottomWidth, -halfHeight, -halfDepth,
         -halfBottomWidth, -halfHeight, -halfDepth
     ]);
     
     // Define the faces (triangles)
     const indices = [
         // Top face
         0, 1, 2,
         0, 2, 3,
         
         // Bottom face
         4, 6, 5,
         4, 7, 6,
         
         // Side faces
         0, 3, 7,
         0, 7, 4,
         
         1, 5, 6,
         1, 6, 2,
         
         0, 4, 5,
         0, 5, 1,
         
         3, 2, 6,
         3, 6, 7
     ];
     
     // Add normals
     const normals = [];
     for (let i = 0; i < vertices.length / 3; i++) {
         normals.push(0, 1, 0); // Simplified - just pointing up
     }
     
     // Set attributes
     geometry.setAttribute('position', new THREE.BufferAttribute(vertices, 3));
     geometry.setAttribute('normal', new THREE.BufferAttribute(new Float32Array(normals), 3));
     geometry.setIndex(indices);
     
     // Compute vertex normals for better lighting
     geometry.computeVertexNormals();
     
     return geometry;
 }

 // Function to convert 2D screen coordinates to 3D world position
 function getDropPosition(event) {
     // Get viewer dimensions and position
     const viewer = document.getElementById('threejs-viewer');
     if (!viewer) return new THREE.Vector3(0, 0, 0);
     
     const rect = viewer.getBoundingClientRect();
     
     // Calculate normalized coordinates
     const normalizedX = ((event.clientX - rect.left) / rect.width) * 2 - 1;
     const normalizedY = -((event.clientY - rect.top) / rect.height) * 2 + 1;
     
     // Create a ray from the camera
     const raycaster = new THREE.Raycaster();
     raycaster.setFromCamera({ x: normalizedX, y: normalizedY }, camera);
     
     // Check for intersections with the floor or existing objects
     const intersects = raycaster.intersectObjects(scene.children, true);
     
     // If we hit something, return that position
     if (intersects.length > 0) {
         return intersects[0].point;
     }
     
     // Default position if no intersection found
     // Project a point at the ground level (y=0)
     const defaultDistance = 5;
     return new THREE.Vector3(
         camera.position.x + raycaster.ray.direction.x * defaultDistance,
         0, // Ground level
         camera.position.z + raycaster.ray.direction.z * defaultDistance
     );
 }

 // Show the object manipulation toolbar
 function showObjectToolbar() {
     const toolbar = document.getElementById('object-toolbar');
     if (toolbar) {
         toolbar.classList.add('visible');
     }
 }

 // Hide the object manipulation toolbar
 function hideObjectToolbar() {
     const toolbar = document.getElementById('object-toolbar');
     if (toolbar) {
         toolbar.classList.remove('visible');
         
         // Reset all tool buttons
         document.querySelectorAll('.tool-btn').forEach(btn => {
             btn.classList.remove('active');
         });
     }
 }

 // Initialize object manipulation tools
 function initObjectTools() {
    console.log("Initializing object tools");
    
    // Rotation tools
    document.getElementById('tool-rotate-x')?.addEventListener('click', () => startTransform('rotate', 'x'));
    document.getElementById('tool-rotate-y')?.addEventListener('click', () => startTransform('rotate', 'y'));
    document.getElementById('tool-rotate-z')?.addEventListener('click', () => startTransform('rotate', 'z'));
    
    // Movement tools
    document.getElementById('tool-move-x')?.addEventListener('click', () => startTransform('move', 'x'));
    document.getElementById('tool-move-y')?.addEventListener('click', () => startTransform('move', 'y'));
    document.getElementById('tool-move-z')?.addEventListener('click', () => startTransform('move', 'z'));
    
    // Delete tool - use a more direct approach without an event handler function
    const deleteBtn = document.getElementById('tool-delete');
    console.log("Delete button element:", deleteBtn);
    
    if (deleteBtn) {
        console.log("Delete button found, adding click listener");
        
        // Remove any existing event listeners if there might be duplicates
        deleteBtn.removeEventListener('click', deleteSelectedObject);
        
        // Add a simple direct click handler
        deleteBtn.onclick = function() {
            console.log("Delete button clicked directly");
            if (selectedMeshForEditing) {
                console.log("Deleting selected object:", selectedMeshForEditing.name);
                scene.remove(selectedMeshForEditing);
                
                // Remove from roomMeshesMap if it exists there
                roomPrefixes.forEach(prefix => {
                    if (roomMeshesMap.has(prefix)) {
                        roomMeshesMap.get(prefix).delete(selectedMeshForEditing);
                    }
                });
                
                // Also check Misc category
                if (roomMeshesMap.has(MISC_CATEGORY)) {
                    roomMeshesMap.get(MISC_CATEGORY).delete(selectedMeshForEditing);
                }
                
                console.log(`Deleted object: ${selectedMeshForEditing.name}`);
                
                // Clear selection
                clearSelection();
                
                // Update UI
                populateModelGroupsMenu();
                populateRoomToggles();
            } else {
                console.log("No object selected to delete");
            }
        };
    } else {
        console.error("Delete button element not found!");
    }
    
    // Add mouse move listener for transformation
    renderer.domElement.addEventListener('mousemove', handleTransformMouseMove);
    
    // Add click listener to end transformation
    renderer.domElement.addEventListener('click', endTransform);
    
    // Add escape key listener to cancel transformation
    document.addEventListener('keydown', e => {
        if (e.key === 'Escape') endTransform();
    });
}

 // Start object transformation
 function startTransform(type, axis) {
     if (!selectedMeshForEditing) return;
     
     // If already transforming the same way, end it (toggle behavior)
     if (isTransforming && transformType === type && transformAxis === axis) {
         endTransform();
         return;
     }
     
     // End any previous transformation
     endTransform();
     
     // Set new transformation state
     isTransforming = true;
     transformType = type;
     transformAxis = axis;
     
     // Store initial mouse position
     transformStartPosition.set(mouse.x, mouse.y);
     
     // Highlight the active tool button
     const buttonId = `tool-${type}-${axis}`;
     const button = document.getElementById(buttonId);
     if (button) button.classList.add('active');
     
     // Change cursor
     renderer.domElement.style.cursor = 'move';
     
     console.log(`Started ${type} on ${axis} axis`);
 }

 // Handle mouse movement for transformation
 function handleTransformMouseMove(event) {
     if (!isTransforming || !selectedMeshForEditing) return;
     
     // Get current mouse position
     const rect = renderer.domElement.getBoundingClientRect();
     const currentX = ((event.clientX - rect.left) / rect.width) * 2 - 1;
     const currentY = -((event.clientY - rect.top) / rect.height) * 2 + 1;
     
     // Calculate delta from start position
     const deltaX = currentX - transformStartPosition.x;
     const deltaY = currentY - transformStartPosition.y;
     
     // Use the larger of the deltas for manipulation
     const delta = Math.abs(deltaX) > Math.abs(deltaY) ? deltaX : -deltaY;
     
     // Apply transformation based on type and axis
     if (transformType === 'rotate') {
         rotateObject(selectedMeshForEditing, transformAxis, delta);
     } else if (transformType === 'move') {
         moveObject(selectedMeshForEditing, transformAxis, delta);
     }
     
     // Update start position for next movement
     transformStartPosition.set(currentX, currentY);
 }

 // Rotate the object on the specified axis
 function rotateObject(object, axis, delta) {
     // Scale delta for smoother rotation
     const rotationAmount = delta * Math.PI; // Full circle for full screen drag
     
     // Apply rotation
     switch (axis) {
         case 'x':
             object.rotation.x += rotationAmount;
             break;
         case 'y':
             object.rotation.y += rotationAmount;
             break;
         case 'z':
             object.rotation.z += rotationAmount;
             break;
     }
 }

 // Move the object on the specified axis
 function moveObject(object, axis, delta) {
     // Scale delta for smoother movement
     const moveAmount = delta * 2; // Scale factor for more natural movement
     
     // Apply movement
     switch (axis) {
         case 'x':
             object.position.x += moveAmount;
             break;
         case 'y':
             object.position.y += moveAmount;
             break;
         case 'z':
             object.position.z += moveAmount;
             break;
     }
 }

 // End the current transformation
 function endTransform() {
     if (!isTransforming) return;
     
     // Reset transformation state
     isTransforming = false;
     transformType = null;
     transformAxis = null;
     
     // Reset cursor
     renderer.domElement.style.cursor = 'auto';
     
     // Reset all tool buttons
     document.querySelectorAll('.tool-btn').forEach(btn => {
         btn.classList.remove('active');
     });
     
     console.log('Ended transformation');
 }

 // Delete the selected object
 function deleteSelectedObject() {
    console.log("deleteSelectedObject called, selectedMeshForEditing:", selectedMeshForEditing);
    if (!selectedMeshForEditing) return;
    
    // Remove from scene
    scene.remove(selectedMeshForEditing);
    
    // Remove from roomMeshesMap if it exists there
    roomPrefixes.forEach(prefix => {
        if (roomMeshesMap.has(prefix)) {
            roomMeshesMap.get(prefix).delete(selectedMeshForEditing);
        }
    });
    
    // Also check Misc category
    if (roomMeshesMap.has(MISC_CATEGORY)) {
        roomMeshesMap.get(MISC_CATEGORY).delete(selectedMeshForEditing);
    }
    
    console.log(`Deleted object: ${selectedMeshForEditing.name}`);
    
    // Clear selection
    clearSelection();
    
    // Update UI
    populateModelGroupsMenu();
    populateRoomToggles();
}

 // Initialize when the DOM is ready
 document.addEventListener('DOMContentLoaded', initViewer); 