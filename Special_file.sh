# PintSSv1tt - Photo Finder Setup Script
# This script will set up everything you need to run the Photo Finder.

PROJECT_NAME="PintSSv1tt_Project"
echo "Creating $PROJECT_NAME..."

# 1. Create Folder
mkdir -p "$PROJECT_NAME"
cd "$PROJECT_NAME"

# 2. Create requirements.txt
cat << 'EOF' > requirements.txt
icrawler
pyfiglet
Pillow
EOF

# 3. Copy main script (assuming it's in the parent dir when running this)
if [ -f "../img_ss.py" ]; then
    cp "../img_ss.py" .
else
    echo "Error: img_ss.py not found in parent directory."
    exit 1
fi

# 4. Create a README.md (read if need help :))
cat << 'EOF' > README.md
# PintSSv1tt - Photo Finder

A terminal-based tool to search and download the top 5 images from the web, automatically converting them to PNG with unique naming.

## How to Run

1. Run the setup script:
   ./Special_file.sh
2. Activate environment and run:
   python3 img_ss.py
EOF

# 5. Set up Virtual Environment
echo "Setting up virtual environment..."
python3 -m venv venv
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo "------------------------------------------------"
echo "Setup Complete!"
echo "To run the tool, type:"
echo "cd $PROJECT_NAME && ./venv/bin/python3 img_ss.py"
echo "------------------------------------------------"
