import React from "react";
import { useLocation, Link } from "react-router-dom";
import {
  Card,
  CardHeader,
  CardTitle,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

const Result = () => {
  const { state } = useLocation();
  if (!state)
    return (
      <div className="flex justify-center items-center h-screen">
        <Card className="p-8 shadow-lg rounded-2xl text-center">
          <CardTitle>No data available.</CardTitle>
          <CardContent className="mt-4">
            <Link to="/">
              <Button>Go Back</Button>
            </Link>
          </CardContent>
        </Card>
      </div>
    );

  const {
    uploaded_image_url,
    output_image_url,
    gemini_result,
    detected_objects,
    model_used,
  } = state;

  const isWaste = gemini_result?.is_waste;

  return (
    <div className="flex flex-col items-center py-10 px-4 min-h-screen bg-linear-to-br from-green-50 to-emerald-100">
      <h1 className="text-3xl font-bold text-green-800 mb-6">
        ♻️ Waste Detection Result
      </h1>

      {/* Image Display Section */}
      <div className="flex flex-wrap justify-center gap-10 mb-8">
        {/* Uploaded Image */}
        <Card className="w-[320px] shadow-xl border-2 border-green-200">
          <CardHeader>
            <CardTitle className="text-center text-green-700">
              Uploaded Image
            </CardTitle>
          </CardHeader>
          <CardContent>
            <img
              src={uploaded_image_url}
              alt="Uploaded"
              className="rounded-lg w-fit h-fit object-cover"
            />
          </CardContent>
        </Card>

        {/* Detected Image (only if waste) */}
        {isWaste && (
          <Card className="w-[320px] shadow-xl border-2 border-green-200">
            <CardHeader>
              <CardTitle className="text-center text-green-700">
                Detected Output
              </CardTitle>
            </CardHeader>
            <CardContent>
              <img
                src={output_image_url}
                alt="Output"
                className="rounded-lg w-fit h-fit object-cover"
              />
            </CardContent>
          </Card>
        )}
      </div>

      {/* Gemini Analysis Card */}
      <Card className="max-w-3xl w-full bg-white/70 backdrop-blur-md shadow-lg border border-green-200">
        <CardHeader>
          <CardTitle className="text-xl text-green-800">
             AI Analysis
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-2 text-gray-700">
          <p>
            <span className="font-semibold">Waste Type:</span>{" "}
            {gemini_result?.waste_type || "N/A"}
          </p>
          <p>
            <span className="font-semibold">Description:</span>{" "}
            {gemini_result?.description || "No details available."}
          </p>
          <p>
            <span className="font-semibold">Disposal Advice:</span>{" "}
            {gemini_result?.disposal_advice || "N/A"}
          </p>
        </CardContent>
        {isWaste && (
          <CardFooter className="text-sm text-gray-600">
            <div>
              <p>
                <span className="font-semibold">Detected Objects:</span>{" "}
                {detected_objects?.length > 0
                  ? detected_objects.join(", ")
                  : "No objects detected."}
              </p>
              <p>
                <span className="font-semibold">Model Used:</span> {model_used}
              </p>
            </div>
          </CardFooter>
        )}
      </Card>

      {/* Back Button */}
      <div className="mt-8">
        <Link to="/">
          <Button className="bg-green-700 hover:bg-green-800 text-white px-6 py-2 rounded-xl shadow-md">
            Upload Another Image
          </Button>
        </Link>
      </div>
    </div>
  );
};

export default Result;
