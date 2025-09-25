import React, { useState, useRef } from "react";
import { motion } from "framer-motion";
import { Upload, FileText, AlertCircle } from "lucide-react";

interface FileUploaderProps {
  onFilesUploaded: (files: File[]) => void;
}

export const FileUploader: React.FC<FileUploaderProps> = ({
  onFilesUploaded,
}) => {
  const [isDragging, setIsDragging] = useState(false);
  const [isUploading, setIsUploading] = useState(false);
  const [error, setError] = useState<string>("");
  const fileInputRef = useRef<HTMLInputElement>(null);

  const allowedTypes = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/jpg",
  ];
  const maxFileSize = 10 * 1024 * 1024; // 10MB

  const validateFile = (file: File): string | null => {
    if (!allowedTypes.includes(file.type)) {
      return "Please upload only PDF or image files (JPEG, PNG)";
    }
    if (file.size > maxFileSize) {
      return "File size must be less than 10MB";
    }
    return null;
  };

  const handleFiles = async (files: FileList | null) => {
    if (!files || files.length === 0) return;

    setError("");
    const fileArray = Array.from(files);

    // Validate all files
    for (const file of fileArray) {
      const validationError = validateFile(file);
      if (validationError) {
        setError(validationError);
        return;
      }
    }

    setIsUploading(true);

    try {
      // Simulate upload delay
      await new Promise((resolve) => setTimeout(resolve, 1000));
      onFilesUploaded(fileArray);
    } catch {
      setError("Failed to upload files. Please try again.");
    } finally {
      setIsUploading(false);
    }
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    handleFiles(e.dataTransfer.files);
  };

  const handleFileSelect = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    handleFiles(e.target.files);
  };

  return (
    <div className="space-y-4">
      {/* Drag and Drop Area */}
      <motion.div
        animate={{
          borderColor: isDragging ? "#76B3A8" : "#D1D5DB",
          backgroundColor: isDragging ? "#F0FDF4" : "#FAFAFA",
        }}
        onDragOver={handleDragOver}
        onDragLeave={handleDragLeave}
        onDrop={handleDrop}
        className={`relative border-2 border-dashed rounded-xl p-8 text-center transition-all cursor-pointer ${
          isUploading
            ? "pointer-events-none opacity-50"
            : "hover:border-[#76B3A8] hover:bg-gray-50"
        }`}
        onClick={handleFileSelect}
      >
        <input
          ref={fileInputRef}
          type="file"
          multiple
          accept=".pdf,.jpg,.jpeg,.png"
          onChange={handleFileChange}
          className="hidden"
        />

        {isUploading ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            className="flex flex-col items-center space-y-3"
          >
            <div className="w-12 h-12 border-4 border-[#76B3A8] border-t-transparent rounded-full animate-spin"></div>
            <p className="text-sm text-gray-600">Uploading files...</p>
          </motion.div>
        ) : (
          <div className="flex flex-col items-center space-y-3">
            <div className="w-12 h-12 bg-[#76B3A8]/10 rounded-full flex items-center justify-center">
              <Upload className="w-6 h-6 text-[#76B3A8]" />
            </div>
            <div>
              <p className="text-sm font-medium text-gray-900">
                Drop your lab reports here, or{" "}
                <span className="text-[#76B3A8] underline">browse</span>
              </p>
              <p className="text-xs text-gray-500 mt-1">
                PDF, JPEG, PNG up to 10MB
              </p>
            </div>
          </div>
        )}
      </motion.div>

      {/* Error Message */}
      {error && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center space-x-2 p-3 bg-red-50 border border-red-200 rounded-lg text-red-700"
        >
          <AlertCircle className="w-5 h-5 flex-shrink-0" />
          <span className="text-sm">{error}</span>
        </motion.div>
      )}

      {/* Upload Button */}
      <motion.button
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        onClick={handleFileSelect}
        disabled={isUploading}
        className="w-full flex items-center justify-center space-x-2 bg-[#76B3A8] text-white py-3 px-4 rounded-lg hover:bg-[#6ba396] disabled:opacity-50 disabled:cursor-not-allowed transition-all"
      >
        <FileText className="w-5 h-5" />
        <span>Browse Files</span>
      </motion.button>
    </div>
  );
};
