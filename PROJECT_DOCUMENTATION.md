# SmartSeg - AI-Driven Smart Waste Segregation with E-Waste Integration

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Project Structure](#project-structure)
5. [Backend Architecture](#backend-architecture)
6. [Frontend Architecture](#frontend-architecture)
7. [AI Models & Detection System](#ai-models--detection-system)
8. [Data Flow & Processing](#data-flow--processing)
9. [API Endpoints](#api-endpoints)
10. [Setup & Installation](#setup--installation)
11. [How It Works (Step-by-Step)](#how-it-works-step-by-step)
12. [Key Features](#key-features)
13. [Development Notes](#development-notes)

---

## 🎯 Project Overview

**SmartSeg** is an intelligent waste classification and segregation system that combines **Computer Vision (YOLO)** and **Generative AI (Google Gemini)** to identify, classify, and provide disposal advice for different types of waste.

### Main Objectives:
- **Automated Waste Detection**: Identify waste objects in uploaded images
- **Multi-Category Classification**: Classify waste as E-waste, BioDegradable, Non-Biodegradable, or Mixed
- **Smart Disposal Guidance**: Provide AI-generated advice for proper waste disposal
- **Visual Object Detection**: Draw bounding boxes around detected waste items
- **User-Friendly Interface**: Simple upload-analyze-result workflow

### Use Cases:
- Home waste segregation assistance
- Educational tool for waste management
- Integration into smart city waste management systems
- E-waste recycling facility preprocessing

---

## 🏗️ System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER                                │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (React + Vite)                  │
│  ┌─────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Upload    │→ │    Result    │  │   Navbar     │      │
│  │  Component  │  │  Component   │  │  Component   │      │
│  └─────────────┘  └──────────────┘  └──────────────┘      │
│         │                  ▲                                │
│         │ POST /detect     │ Display Results               │
└─────────┼──────────────────┼────────────────────────────────┘
          │                  │
          ▼                  │
┌─────────────────────────────────────────────────────────────┐
│                   BACKEND (Flask)                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              /detect Endpoint                        │  │
│  └───────┬──────────────────────────────────────────────┘  │
│          │                                                  │
│          ▼                                                  │
│  ┌──────────────────────┐        ┌────────────────────┐   │
│  │  Gemini AI Analysis  │        │   YOLO Detection   │   │
│  │  (Waste Classifier)  │───────→│   (Object Detect)  │   │
│  └──────────────────────┘        └────────────────────┘   │
│          │                                │                 │
│          │  Determines Model Type         │                 │
│          └────────────────────────────────┘                 │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │           Model Selection Logic                      │  │
│  │  • YOLOv8 (E-waste) - best_e.pt                      │  │
│  │  • YOLOv5 (Waste) - best.pt                          │  │
│  │  • YOLOv8 (Mixed) - bestmix.pt                       │  │
│  └──────────────────────────────────────────────────────┘  │
│                         │                                   │
│                         ▼                                   │
│  ┌──────────────────────────────────────────────────────┐  │
│  │  Save Images & Generate Response                     │  │
│  │  • Upload: static/uploads/                           │  │
│  │  • Output: static/output/                            │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
```

### Architecture Layers:

1. **Presentation Layer (Frontend)**
   - React-based UI components
   - Client-side routing with React Router
   - TailwindCSS styling with custom components

2. **API Layer (Backend)**
   - Flask REST API
   - CORS enabled for cross-origin requests
   - File upload and management

3. **AI/ML Layer**
   - Google Gemini 2.5 Flash for classification
   - YOLOv8 for E-waste and Mixed waste detection
   - YOLOv5 for general waste detection

4. **Storage Layer**
   - Static file storage for uploads and outputs
   - CSV logging for waste detection records

---

## 🛠️ Technology Stack

### Frontend
| Technology | Version | Purpose |
|------------|---------|---------|
| **React** | 18.3.1 | UI framework |
| **Vite** | 7.1.7 | Build tool and dev server |
| **TypeScript** | 5.9.3 | Type safety |
| **React Router** | 6.30.1 | Client-side routing |
| **TailwindCSS** | 4.1.16 | Styling framework |
| **Axios** | 1.13.5 | HTTP client |
| **Lucide React** | 0.552.0 | Icon library |
| **Radix UI** | Latest | Accessible UI components |

### Backend
| Technology | Version/Type | Purpose |
|------------|--------------|---------|
| **Flask** | Latest | Web framework |
| **PyTorch** | Latest | Deep learning framework |
| **Ultralytics YOLO** | Latest | Object detection (YOLOv8) |
| **YOLOv5** | Custom | Object detection (general waste) |
| **Google Gemini** | 2.5 Flash | AI classification |
| **OpenCV (cv2)** | Latest | Image processing |
| **Pillow (PIL)** | Latest | Image manipulation |
| **Flask-CORS** | Latest | Cross-origin support |
| **Pandas** | Latest | Data manipulation |

### AI Models
| Model | File | Purpose | Format |
|-------|------|---------|--------|
| **E-waste Detector** | `best_e.pt` | Detects electronic waste items | YOLOv8 |
| **General Waste** | `best.pt` | Detects biodegradable/non-biodegradable waste | YOLOv5 |
| **Mixed Waste** | `bestmix.pt` | Detects both e-waste and general waste | YOLOv8 |
| **YOLOv5 Repository** | `yolov5/` | YOLOv5 model architecture | PyTorch Hub |

---

## 📁 Project Structure

```
SmartSeg/
│
├── backend/                          # Flask backend server
│   ├── app.py                       # Main Flask application
│   ├── model/                       # AI models directory
│   │   ├── best_e.pt               # YOLOv8 E-waste model (6.25 MB)
│   │   ├── best.pt                 # YOLOv5 General waste model (14.47 MB)
│   │   ├── bestmix.pt              # YOLOv8 Mixed waste model (6.26 MB)
│   │   ├── best_ewaste.pt          # Alternative E-waste model (14.85 MB)
│   │   └── yolov5/                 # YOLOv5 repository (29 files)
│   ├── static/                      # Static file storage
│   │   ├── uploads/                # User uploaded images
│   │   └── output/                 # Processed images with detections
│   └── waste_log.csv               # Detection log file
│
├── frontend/                         # React frontend application
│   ├── public/                      # Public static assets
│   ├── src/                         # Source code
│   │   ├── components/             # React components
│   │   │   ├── ui/                 # Reusable UI components
│   │   │   │   ├── button.jsx     # Custom button component
│   │   │   │   └── card.jsx       # Custom card component
│   │   │   ├── Upload.jsx         # Upload page component
│   │   │   ├── Result.jsx         # Result display component
│   │   │   ├── Navbar.jsx         # Navigation bar
│   │   │   └── N.tsx              # Additional component
│   │   ├── lib/                    # Utility libraries
│   │   ├── assets/                 # Images, fonts, etc.
│   │   ├── App.jsx                 # Main app component
│   │   ├── main.jsx                # Entry point
│   │   ├── index.css               # Global styles
│   │   └── App.css                 # App-specific styles
│   ├── index.html                   # HTML template
│   ├── package.json                 # Dependencies
│   ├── vite.config.ts              # Vite configuration
│   ├── tsconfig.json                # TypeScript config
│   ├── components.json              # Shadcn/ui config
│   └── README.md                    # Frontend documentation
│
└── PROJECT_DOCUMENTATION.md         # This file
```

---

## 🔧 Backend Architecture

### Main Application (`app.py`)

#### 1. **Initialization & Configuration**
```python
# Windows compatibility for pathlib
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath

# Flask app setup
app = Flask(__name__)
CORS(app)  # Enable cross-origin requests

# Directory configuration
UPLOAD_FOLDER = 'static/uploads'
OUTPUT_FOLDER = 'static/output'
```

#### 2. **AI Model Loading**
Three models are loaded at startup:
- **`model_ewaste`**: YOLOv8 for E-waste (`best_e.pt`)
- **`model_waste`**: YOLOv5 for general waste (`best.pt`)
- **`model_mixed`**: YOLOv8 for mixed waste (`bestmix.pt`)

#### 3. **Gemini AI Integration**

**Function**: `gemini_analyze_image(image_path)`

**Purpose**: Initial waste classification using Google's Gemini 2.5 Flash model

**Process**:
1. Reads image as base64-encoded data
2. Sends to Gemini with strict JSON prompt
3. Receives classification result:
   ```json
   {
     "is_waste": true/false,
     "waste_type": "E-waste | BioDegradable | Non-Biodegradable | Mixed | Not Waste",
     "description": "Explanation of classification",
     "disposal_advice": "How to dispose of this waste"
   }
   ```
4. Parses JSON response (handles markdown code blocks)
5. Returns structured result

**Error Handling**:
- JSON parsing errors return null values
- Logs raw Gemini response for debugging

#### 4. **Detection Endpoint**

**Route**: `POST /detect`

**Content-Type**: `multipart/form-data`

**Request**:
- **Field**: `file`
- **Type**: Image file (JPEG, PNG, etc.)

**Response**:
```json
{
  "gemini_result": {
    "is_waste": true,
    "waste_type": "E-waste",
    "description": "Electronic components detected",
    "disposal_advice": "Take to certified e-waste recycling center"
  },
  "uploaded_image_url": "http://127.0.0.1:5000/static/uploads/image.jpg",
  "output_image_url": "http://127.0.0.1:5000/static/output/output_1234567890.jpg",
  "detected_objects": ["laptop", "phone", "battery"],
  "model_used": "YOLOv8 (E-waste)",
  "final_advice": "Take to certified e-waste recycling center"
}
```

**Processing Flow**:

1. **File Upload**
   - Validate file presence
   - Save to `static/uploads/`

2. **Gemini Classification**
   - Analyze image with Gemini AI
   - Determine waste type

3. **Model Selection Logic**
   ```
   IF waste_type contains "mixed" OR ("e-waste" AND "non-biodegradable")
       → Use model_mixed (YOLOv8 Mixed)
   ELSE IF waste_type contains "e-waste"
       → Use model_ewaste (YOLOv8 E-waste)
   ELSE
       → Use model_waste (YOLOv5 General Waste)
   ```

4. **Object Detection**
   - **YOLOv8 Models**:
     - Run prediction with confidence threshold 0.25
     - IoU threshold 0.35
     - Generate annotated image with bounding boxes
     - Extract detected object names
   
   - **YOLOv5 Model**:
     - Convert image to RGB if needed
     - Run inference
     - Render detection results
     - Extract object classes

5. **Result Generation**
   - Save output image with timestamp
   - Compile detection results
   - Return comprehensive JSON response

---

## 🎨 Frontend Architecture

### Component Hierarchy

```
main.jsx (Entry Point)
  └── BrowserRouter
      ├── Navbar (Always visible)
      └── App.jsx
          └── Routes
              ├── / → Upload Component
              └── /result → Result Component
```

### Components Deep Dive

#### 1. **Upload Component** (`Upload.jsx`)

**Purpose**: Image upload and submission interface

**State Management**:
- `file`: Selected image file
- `error`: Error messages
- `loading`: Loading state during API call

**Key Features**:
- Image preview before upload
- File selection validation
- Loading indicator during processing
- Error display

**User Flow**:
1. User clicks "Choose File" button
2. File input opens (accepts `image/*`)
3. Image preview displays
4. User clicks "Analyze" button
5. FormData sent to backend via Axios POST
6. On success: Navigate to `/result` with response data
7. On error: Display error message

**Styling**:
- Emerald green theme
- Card-based layout with shadow
- Responsive design
- Lucide icons for visual enhancement

#### 2. **Result Component** (`Result.jsx`)

**Purpose**: Display detection results and analysis

**Data Source**: `useLocation()` state from React Router

**Layout Sections**:

1. **Image Comparison**
   - Original uploaded image (always shown)
   - Detected output image (only if waste detected)

2. **AI Analysis Card**
   - Waste type classification
   - Detailed description
   - Disposal advice

3. **Detection Details** (if waste detected)
   - List of detected objects
   - Model used for detection

4. **Navigation**
   - "Upload Another Image" button

**Error Handling**:
- Displays fallback UI if no data available
- Provides "Go Back" option

#### 3. **Navbar Component** (`Navbar.jsx`)

**Purpose**: Application title/branding

**Content**: "AI-Driven Smart Waste Segregation with E-Waste Integration"

**Styling**: Dark green header with centered text

#### 4. **UI Components** (`components/ui/`)

**Card Components** (`card.jsx`):
- `Card`: Container with border and shadow
- `CardHeader`: Header section
- `CardTitle`: Title styling
- `CardContent`: Main content area
- `CardFooter`: Footer section

**Button Component** (`button.jsx`):
- Radix UI based
- Multiple variants support
- Class variance authority for styling

### Routing

**Routes Defined**:
- `/` → Upload page (home)
- `/result` → Result display page

**Navigation Method**: React Router's `useNavigate()` with state passing

---

## 🤖 AI Models & Detection System

### Model Comparison

| Aspect | YOLOv8 (E-waste & Mixed) | YOLOv5 (General Waste) |
|--------|-------------------------|------------------------|
| **Architecture** | Ultralytics YOLOv8 | PyTorch Hub YOLOv5 |
| **Loading Method** | `YOLO(model_path)` | `torch.hub.load()` |
| **Inference** | `model.predict()` | `model(image)` |
| **Output Format** | Results object with boxes | XY coordinates with labels |
| **Visualization** | `results[0].plot()` | `results.render()[0]` |
| **Confidence** | 0.25 | Default |
| **IoU Threshold** | 0.35 | Default |
| **File Size** | ~6 MB | ~14 MB |

### Detection Classes

**E-waste Model** likely detects:
- Electronics (phones, laptops, tablets)
- Batteries
- Cables and chargers
- Circuit boards
- Monitors and screens

**General Waste Model** likely detects:
- Plastic bottles and containers
- Paper and cardboard
- Glass bottles
- Organic waste (food scraps)
- Metal cans
- Non-recyclable items

**Mixed Waste Model**:
- Combination of both categories
- Handles images with multiple waste types

### Gemini AI Classification

**Model**: `gemini-2.5-flash`

**Capabilities**:
- Visual understanding of waste images
- Context-aware classification
- Natural language reasoning
- Multi-category detection

**Prompt Engineering**:
- Strict JSON formatting requirement
- Explicit schema definition
- Error handling for markdown responses

**Classification Categories**:
1. **E-waste**: Electronic devices and components
2. **BioDegradable Waste**: Organic, compostable materials
3. **Non-Biodegradable Waste**: Plastics, metals, glass
4. **Mixed Waste**: Combination of categories
5. **Not Waste**: Non-waste items

---

## 🔄 Data Flow & Processing

### Complete Request-Response Cycle

```
[USER UPLOADS IMAGE]
        │
        ▼
┌───────────────────────┐
│  Frontend (Upload)    │
│  • File selected      │
│  • Preview shown      │
└───────┬───────────────┘
        │ FormData
        │ POST /detect
        ▼
┌───────────────────────┐
│  Backend Receives     │
│  • Validate file      │
│  • Save to uploads/   │
└───────┬───────────────┘
        │ Image path
        ▼
┌───────────────────────┐
│  Gemini Analysis      │
│  • Encode base64      │
│  • Send to Gemini API │
│  • Parse JSON response│
└───────┬───────────────┘
        │ Classification result
        ▼
┌───────────────────────┐
│  Model Selection      │
│  • Check waste_type   │
│  • Select appropriate │
│    YOLO model         │
└───────┬───────────────┘
        │ Selected model
        ▼
┌───────────────────────┐
│  Object Detection     │
│  • Run inference      │
│  • Draw bounding boxes│
│  • Extract objects    │
│  • Save output image  │
└───────┬───────────────┘
        │ Detection results
        ▼
┌───────────────────────┐
│  Response Assembly    │
│  • Compile all data   │
│  • Generate URLs      │
│  • Create JSON        │
└───────┬───────────────┘
        │ JSON response
        ▼
┌───────────────────────┐
│  Frontend (Result)    │
│  • Parse response     │
│  • Display images     │
│  • Show analysis      │
│  • Render advice      │
└───────────────────────┘
        │
        ▼
   [USER SEES RESULTS]
```

### Data Transformations

1. **Image Upload**:
   - Original format (JPEG/PNG) → FormData → Backend file system

2. **Gemini Processing**:
   - Image file → Base64 string → Gemini API → JSON response

3. **YOLO Detection**:
   - Image file → PIL/CV2 image → Tensor → Model inference → Annotated image

4. **Response Compilation**:
   - Multiple data sources → Single JSON object → Frontend state

---

## 🔌 API Endpoints

### POST /detect

**Description**: Upload an image for waste detection and classification

**Request**:
```http
POST http://127.0.0.1:5000/detect
Content-Type: multipart/form-data

file: [IMAGE_FILE]
```

**Success Response (200)**:
```json
{
  "gemini_result": {
    "is_waste": true,
    "waste_type": "E-waste",
    "description": "The image contains electronic waste including circuit boards and batteries",
    "disposal_advice": "Take to certified e-waste recycling facility. Do not dispose in regular trash."
  },
  "uploaded_image_url": "http://127.0.0.1:5000/static/uploads/phone.jpg",
  "output_image_url": "http://127.0.0.1:5000/static/output/output_1707478890.jpg",
  "detected_objects": ["phone", "battery", "charger"],
  "model_used": "YOLOv8 (E-waste)",
  "final_advice": "Take to certified e-waste recycling facility. Do not dispose in regular trash."
}
```

**Non-Waste Response (200)**:
```json
{
  "gemini_result": {
    "is_waste": false,
    "waste_type": "Not Waste",
    "description": "This is a decorative item, not waste",
    "disposal_advice": "No disposal needed"
  },
  "uploaded_image_url": "http://127.0.0.1:5000/static/uploads/vase.jpg",
  "output_image_url": null,
  "message": "The object is not waste.",
  "detected_objects": [],
  "model_used": null,
  "final_advice": "No disposal needed"
}
```

**Error Responses**:

```json
// 400 - No file uploaded
{
  "error": "No file uploaded"
}

// 400 - Empty filename
{
  "error": "No file selected"
}

// 500 - Server error
{
  "error": "Error message details"
}
```

### Static File Serving

**Uploaded Images**:
```
GET http://127.0.0.1:5000/static/uploads/{filename}
```

**Output Images**:
```
GET http://127.0.0.1:5000/static/output/{filename}
```

---

## ⚙️ Setup & Installation

### Prerequisites

**Backend**:
- Python 3.8+
- pip package manager
- CUDA-compatible GPU (optional, for faster inference)

**Frontend**:
- Node.js 16+
- npm or yarn

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install flask flask-cors torch ultralytics pillow opencv-python pandas google-generativeai
   ```

4. **Configure Gemini API**:
   - Obtain API key from Google AI Studio
   - Replace in `app.py` line 19:
     ```python
     client = genai.Client(api_key="YOUR_API_KEY_HERE")
     ```

5. **Verify model files**:
   - Ensure `model/best_e.pt`, `model/best.pt`, `model/bestmix.pt` exist
   - Ensure `model/yolov5/` directory is present

6. **Run backend server**:
   ```bash
   python app.py
   ```
   - Server starts at `http://127.0.0.1:5000`
   - Debug mode enabled by default

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure backend URL** (if different):
   - Update in `src/components/Upload.jsx` line 26
   - Default: `http://127.0.0.1:5000/detect`

4. **Run development server**:
   ```bash
   npm run dev
   ```
   - Vite server starts at `http://localhost:5173` (default)

5. **Build for production** (optional):
   ```bash
   npm run build
   ```

### Running Both Servers

**Option 1: Two Terminal Windows**
```bash
# Terminal 1 - Backend
cd backend
python app.py

# Terminal 2 - Frontend
cd frontend
npm run dev
```

**Option 2: Background Processes** (Windows PowerShell)
```powershell
# Start backend in background
Start-Process python -ArgumentList "app.py" -WorkingDirectory "backend"

# Start frontend
cd frontend
npm run dev
```

---

## 📖 How It Works (Step-by-Step)

### User Perspective

1. **Open Application**
   - Navigate to `http://localhost:5173`
   - See upload interface with title "Upload an Image for Detection"

2. **Select Image**
   - Click "Choose File" button
   - Select an image from file system
   - Preview appears immediately

3. **Analyze Image**
   - Click "Analyze" button
   - Loading spinner appears with "Analyzing..." text

4. **View Results**
   - Redirected to `/result` page
   - See original and detected images side-by-side
   - Read AI analysis including:
     - Waste type classification
     - Detailed description
     - Disposal advice
     - Detected objects (if applicable)

5. **Upload Another**
   - Click "Upload Another Image" to return to upload page

### System Perspective

#### Phase 1: Image Upload
1. User selects file via file input
2. React state updates with file object
3. Preview generated using `URL.createObjectURL()`
4. FormData object created on submit
5. Axios POST request to backend

#### Phase 2: Backend Processing
1. Flask receives multipart/form-data request
2. File validated (presence and filename)
3. File saved to `static/uploads/` with original name
4. Full file path constructed

#### Phase 3: AI Classification (Gemini)
1. Image read as binary data
2. Encoded to base64 string
3. Sent to Gemini API with structured prompt
4. Gemini analyzes image content
5. Returns JSON classification
6. JSON parsed (handles markdown code blocks)
7. `waste_type` extracted

#### Phase 4: Model Selection
```python
if "mixed" in waste_type or ("e-waste" in waste_type and "non-biodegradable" in waste_type):
    model = model_mixed  # YOLOv8 Mixed
    model_type = "YOLOv8 (Mixed Waste)"
elif "e-waste" in waste_type:
    model = model_ewaste  # YOLOv8 E-waste
    model_type = "YOLOv8 (E-waste)"
else:
    model = model_waste  # YOLOv5 General
    model_type = "YOLOv5 (Waste)"
```

#### Phase 5: Object Detection

**For YOLOv8 Models**:
1. Run `model.predict()` with confidence and IoU thresholds
2. Get results object
3. Plot bounding boxes with labels: `results[0].plot()`
4. Convert RGB to BGR for OpenCV compatibility
5. Save annotated image with timestamp
6. Extract class labels from `boxes.cls`

**For YOLOv5 Model**:
1. Open image with PIL
2. Ensure RGB format
3. Run model inference: `model(img)`
4. Render detections: `results.render()[0]`
5. Save as PIL image
6. Extract classes from `results.xywh[0][:, -1]`

#### Phase 6: Response Assembly
1. Compile all data:
   - Gemini result (classification, description, advice)
   - Upload URL (static/uploads/)
   - Output URL (static/output/)
   - Detected objects list
   - Model type used
2. Convert to JSON
3. Return 200 response

#### Phase 7: Frontend Display
1. React Router navigation with state
2. `Result` component receives data via `useLocation()`
3. Parse response object
4. Render image comparison
5. Display AI analysis card
6. Show detection details
7. Provide navigation back to upload

---

## ✨ Key Features

### 1. **Hybrid AI System**
- **Gemini AI**: High-level classification and reasoning
- **YOLO Models**: Precise object detection and localization
- **Synergy**: Gemini determines context, YOLO provides details

### 2. **Multi-Model Architecture**
- Specialized models for different waste types
- Dynamic model selection based on classification
- Optimized inference for each category

### 3. **Real-Time Processing**
- Fast upload and analysis
- Immediate visual feedback
- Progress indicators for user experience

### 4. **Comprehensive Results**
- Before/after image comparison
- Bounding box visualization
- Detailed disposal guidance
- Object-level detection

### 5. **User-Friendly Interface**
- Clean, modern design
- Responsive layout
- Clear visual hierarchy
- Error handling and validation

### 6. **Scalable Design**
- Modular component structure
- Separation of concerns (frontend/backend)
- RESTful API design
- Easy model updates

### 7. **Error Resilience**
- Gemini parsing fallbacks
- File validation
- User feedback for errors
- Graceful degradation

---

## 🔍 Development Notes

### Important Considerations

#### 1. **Windows Compatibility**
```python
temp = pathlib.PosixPath
pathlib.PosixPath = pathlib.WindowsPath
```
This workaround ensures YOLO models work on Windows systems.

#### 2. **Model Paths**
All model paths are **absolute** and **Windows-specific**:
```python
YOLOV8_MODEL_PATH = r"C:\Users\Ayush Sharma\OneDrive\Desktop\SmartSeg\backend\model\best_e.pt"
```
**Action Required**: Update these paths for deployment on other systems.

#### 3. **CORS Configuration**
Frontend and backend run on different ports, requiring CORS:
```python
CORS(app)  # Allows all origins
```
**Production Note**: Restrict origins for security.

#### 4. **Static File Serving**
Images served directly from Flask:
```
http://127.0.0.1:5000/static/uploads/filename.jpg
http://127.0.0.1:5000/static/output/output_timestamp.jpg
```

#### 5. **Timestamp-Based Naming**
Output files use Unix timestamps to avoid collisions:
```python
timestamp = int(time.time())
output_filename = f"output_{timestamp}.jpg"
```

#### 6. **Gemini API Key**
Currently hardcoded in `app.py`:
```python
client = genai.Client(api_key="AIzaSyBh...")
```
**Security Risk**: Move to environment variables for production.

#### 7. **Model Loading**
Models loaded at startup, not per-request:
```python
model_ewaste = YOLO(YOLOV8_MODEL_PATH)
model_waste = torch.hub.load(YOLOV5_MODEL_DIR, 'custom', ...)
model_mixed = YOLO(MIXED_MODEL_PATH)
```
**Benefit**: Faster inference, but higher memory usage.

#### 8. **React Router State Passing**
Results passed via navigation state, not URL params:
```javascript
navigate("/result", { state: res.data })
```
**Limitation**: Data lost on page refresh.

#### 9. **Image Format Handling**
YOLOv5 requires RGB images:
```python
if img.mode != "RGB":
    img = img.convert("RGB")
```

#### 10. **Detection Thresholds**
YOLOv8 uses custom confidence and IoU:
```python
results = model.predict(image, conf=0.25, iou=0.35)
```
**Tuning**: Adjust for accuracy vs. detection coverage.

### Future Enhancements

1. **Database Integration**
   - Store detection history
   - User accounts and sessions
   - Analytics dashboard

2. **Batch Processing**
   - Multiple image upload
   - Folder scanning
   - CSV export of results

3. **Mobile Application**
   - Native iOS/Android apps
   - Camera integration
   - Offline mode

4. **Enhanced AI**
   - Fine-tuned models for specific waste types
   - Real-time video detection
   - Multi-language support

5. **Deployment**
   - Dockerization
   - Cloud hosting (AWS, GCP, Azure)
   - CDN for static files
   - Environment-based configuration

6. **Security**
   - API authentication
   - Rate limiting
   - Input sanitization
   - Environment variables for secrets

7. **Performance**
   - Model quantization for faster inference
   - Image compression
   - Lazy loading
   - Caching strategies

---

## 📊 Technical Specifications

### Performance Metrics
- **Average Processing Time**: 3-8 seconds per image
  - Gemini classification: 1-3 seconds
  - YOLO detection: 1-3 seconds
  - Image processing: 0.5-2 seconds

### Resource Requirements
- **Backend Memory**: ~2-4 GB (with models loaded)
- **GPU Memory**: ~1.5 GB (if CUDA available)
- **Disk Space**:
  - Models: ~35 MB total
  - Dependencies: ~2 GB
  - Runtime storage: Grows with uploads

### Supported Image Formats
- JPEG/JPG
- PNG
- BMP
- WebP
- TIFF (converted to RGB)

### Browser Compatibility
- Chrome 90+
- Firefox 88+
- Safari 14+
- Edge 90+

---

## 🎓 Learning Resources

### Understanding YOLO
- [Ultralytics YOLOv8 Docs](https://docs.ultralytics.com/)
- [YOLOv5 GitHub](https://github.com/ultralytics/yolov5)

### Google Gemini
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Generative AI SDK](https://github.com/google/generative-ai-python)

### React & Vite
- [React Documentation](https://react.dev/)
- [Vite Guide](https://vitejs.dev/guide/)
- [React Router](https://reactrouter.com/)

### Flask
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-CORS](https://flask-cors.readthedocs.io/)

---

## 📝 Summary

**SmartSeg** is a full-stack web application that intelligently classifies and detects waste using a combination of Google Gemini AI for high-level classification and YOLO models for precise object detection. The system handles E-waste, biodegradable, non-biodegradable, and mixed waste with specialized models, providing users with visual detection results and actionable disposal advice through a clean, responsive React interface.

**Core Workflow**: Upload → Gemini Classification → Model Selection → YOLO Detection → Visual Results + Disposal Guidance

**Key Innovation**: Hybrid AI approach combining generative AI understanding with computer vision precision for comprehensive waste analysis.
