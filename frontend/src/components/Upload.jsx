import React, { useState } from "react";
import axios from "axios";
import { useNavigate } from "react-router-dom";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Loader2, Upload as UploadIcon } from "lucide-react";

const Upload = () => {
  const [file, setFile] = useState(null);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleUpload = async () => {
    if (!file) {
      setError("Please upload an image first.");
      return;
    }
    setError("");
    setLoading(true);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const res = await axios.post("http://127.0.0.1:5000/detect", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      navigate("/result", { state: res.data });
    } catch (err) {
      setError("Error during detection: " + err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-linear-to-br from-emerald-100 via-white to-emerald-50 flex items-center justify-center px-4">
      <Card className="w-full max-w-md shadow-xl rounded-2xl border border-emerald-200">
        <CardHeader>
          <CardTitle className="text-center text-2xl font-semibold text-emerald-800">
            Upload an Image for Detection
          </CardTitle>
        </CardHeader>

        <CardContent className="flex flex-col items-center gap-4">
          {/* Image Preview */}
          {file && (
            <img
              src={URL.createObjectURL(file)}
              alt="preview"
              className="w-64 h-64 object-cover rounded-xl shadow-md border border-gray-200"
            />
          )}

          {/* Upload Input */}
          <label
            htmlFor="fileInput"
            className="cursor-pointer bg-emerald-600 hover:bg-emerald-700 text-white px-5 py-2 rounded-md flex items-center gap-2"
          >
            <UploadIcon className="w-4 h-4" /> Choose File
          </label>
          <input
            id="fileInput"
            type="file"
            accept="image/*"
            className="hidden"
            onChange={(e) => setFile(e.target.files[0])}
          />

          {/* Analyze Button */}
          <Button
            onClick={handleUpload}
            disabled={loading}
            className="bg-emerald-700 hover:bg-emerald-800 w-full py-2 mt-2"
          >
            {loading ? (
              <div className="flex items-center justify-center gap-2">
                <Loader2 className="animate-spin w-4 h-4" />
                Analyzing...
              </div>
            ) : (
              "Analyze"
            )}
          </Button>

          {error && <p className="text-red-500 text-sm mt-2">{error}</p>}
        </CardContent>
      </Card>
    </div>
  );
};

export default Upload;
