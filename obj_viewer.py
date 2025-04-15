from flask import Blueprint, render_template_string, render_template

# Create a Blueprint
# - Removed template_folder to use app default
# - Added static_url_path for blueprint's static files
obj_viewer_bp = Blueprint('obj_viewer', __name__, 
                          static_folder='static', 
                          static_url_path='/obj-viewer-static', 
                          url_prefix='/obj-viewer')

@obj_viewer_bp.route('/')
def show_obj_viewer():
    # Render the external HTML template file (from app's templates folder)
    return render_template('obj_viewer.html') 