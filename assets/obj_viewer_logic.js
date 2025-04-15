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
                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
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
                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
             }
             else {
                 // For all other materials, ensure they are opaque and write depth
                 currentMaterial.transparent = false;
                 currentMaterial.depthWrite = true;
                 currentMaterial.depthTest = true;
                 currentMaterial.alphaTest = 0.5; // Increase threshold significantly
                 currentMaterial.side = THREE.FrontSide;
             }
        }); // End loop

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

 // Event handler for object selection
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
     if(colorPicker) colorPicker.style.display = 'none';
     if(visibilityButton) visibilityButton.style.display = 'none';
     if(displayElement) displayElement.textContent = 'Clicked: (None)';
      document.querySelectorAll('.model-group-item').forEach(item => {
          item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)'; // Reset menu item background
      });

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
 
 // NEW: Function to create UI controls for a single object (now only for side menu)
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
         const textureOptions = [
             { value: '', text: 'None' },
             { value: 'wood', text: 'Wood' },
             { value: 'carpet', text: 'Carpet' },
             { value: 'porcelain', text: 'Porcelain' },
             { value: 'epoxy', text: 'Epoxy' },
             { value: 'concrete', text: 'Concrete' }
         ];
         textureOptions.forEach(opt => { textureSelect.add(new Option(opt.text, opt.value)); });

         // Set initial texture value
         if (primaryMaterial && primaryMaterial.map) {
             if (primaryMaterial.map.image?.src?.includes('floor.jpg')) textureSelect.value = 'wood';
             else if (primaryMaterial.map.image?.src?.includes('carpet.jpg')) textureSelect.value = 'carpet';
             else if (primaryMaterial.map.image?.src?.includes('porcelain.jpg')) textureSelect.value = 'porcelain';
             else if (primaryMaterial.map.image?.src?.includes('epoxy')) textureSelect.value = 'epoxy';
             else if (primaryMaterial.map.image?.src?.includes('concrete')) textureSelect.value = 'concrete';
             else textureSelect.value = '';
         } else {
             textureSelect.value = '';
         }

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
     const groupsContainer = document.getElementById('model-groups-container');
     // REMOVED: Reference to mainControlsContainer
     if (!groupsContainer) {
          console.error("Required container element 'model-groups-container' not found.");
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
      outlinePass.selectedObjects = [];
      document.querySelectorAll('.model-group-item').forEach(item => { // Only query side menu items
          item.style.backgroundColor = 'rgba(60, 60, 60, 0.7)';
      });
      // REMOVED: Querying/resetting .material-control items

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

      // Highlight the item ONLY in the side menu
      const menuItem = document.getElementById(`groupsContainer-color-${node.uuid}`)?.closest('.model-group-item'); // ID prefix assumes side menu
      if (menuItem) {
           menuItem.style.backgroundColor = 'rgba(80, 80, 80, 0.9)'; // Highlight color
           const menuContainer = document.getElementById('model-groups-menu');
            if (menuContainer) {
                 menuItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
            }
      }
      // REMOVED: Highlighting/scrolling in the removed main controls area
 }
 
  // Handle window resize
// ... existing code ...
              document.addEventListener('DOMContentLoaded', init); 