import React, { useState } from "react";
import { motion } from "framer-motion";
import {
  Download,
  Calendar,
  FileText,
  AlertCircle,
  CheckCircle,
  TrendingUp,
  Upload,
  X,
  Eye,
} from "lucide-react";
import { FileUploader } from "./FileUploader";

interface LabParameter {
  name: string;
  value: string;
  unit: string;
  range: string;
  status: "normal" | "high" | "low" | "attention";
}

interface LabReport {
  id: string;
  name: string;
  date: string;
  parameters: LabParameter[];
  downloadUrl?: string;
  fileName?: string;
}

export const LabReportsTab: React.FC = () => {
  const [uploadedFiles, setUploadedFiles] = useState<
    Array<{ name: string; url: string; type: string }>
  >([]);

  const labReports: LabReport[] = [
    {
      id: "1",
      name: "Complete Blood Count",
      date: "2025-09-20",
      downloadUrl: "#",
      fileName: "CBC_Report_Sep2025.pdf",
      parameters: [
        {
          name: "Hemoglobin",
          value: "14.2",
          unit: "g/dL",
          range: "12.0-15.5",
          status: "normal",
        },
        {
          name: "White Blood Cells",
          value: "7,800",
          unit: "/μL",
          range: "4,000-11,000",
          status: "normal",
        },
        {
          name: "Platelets",
          value: "285,000",
          unit: "/μL",
          range: "150,000-450,000",
          status: "normal",
        },
        {
          name: "Hematocrit",
          value: "42.1",
          unit: "%",
          range: "36.0-46.0",
          status: "normal",
        },
      ],
    },
    {
      id: "2",
      name: "Lipid Panel",
      date: "2025-09-18",
      downloadUrl: "#",
      fileName: "Lipid_Panel_Sep2025.pdf",
      parameters: [
        {
          name: "Total Cholesterol",
          value: "220",
          unit: "mg/dL",
          range: "<200",
          status: "high",
        },
        {
          name: "LDL Cholesterol",
          value: "155",
          unit: "mg/dL",
          range: "<130",
          status: "attention",
        },
        {
          name: "HDL Cholesterol",
          value: "45",
          unit: "mg/dL",
          range: ">40",
          status: "normal",
        },
        {
          name: "Triglycerides",
          value: "180",
          unit: "mg/dL",
          range: "<150",
          status: "high",
        },
      ],
    },
    {
      id: "3",
      name: "Thyroid Function",
      date: "2025-09-15",
      downloadUrl: "#",
      fileName: "Thyroid_Test_Sep2025.pdf",
      parameters: [
        {
          name: "TSH",
          value: "2.1",
          unit: "mIU/L",
          range: "0.4-4.0",
          status: "normal",
        },
        {
          name: "Free T4",
          value: "1.3",
          unit: "ng/dL",
          range: "0.8-1.8",
          status: "normal",
        },
        {
          name: "Free T3",
          value: "3.2",
          unit: "pg/mL",
          range: "2.3-4.2",
          status: "normal",
        },
      ],
    },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case "normal":
        return "text-green-700 bg-green-100 border-green-200";
      case "high":
        return "text-red-700 bg-red-100 border-red-200";
      case "low":
        return "text-yellow-700 bg-yellow-100 border-yellow-200";
      case "attention":
        return "text-orange-700 bg-orange-100 border-orange-200";
      default:
        return "text-gray-700 bg-gray-100 border-gray-200";
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case "normal":
        return <CheckCircle className="w-3 h-3" />;
      case "high":
        return <TrendingUp className="w-3 h-3" />;
      case "low":
        return <TrendingUp className="w-3 h-3 rotate-180" />;
      case "attention":
        return <AlertCircle className="w-3 h-3" />;
      default:
        return <AlertCircle className="w-3 h-3" />;
    }
  };

  const handleFileUpload = (files: File[]) => {
    files.forEach((file) => {
      // In a real app, you would upload to a server
      const url = URL.createObjectURL(file);
      setUploadedFiles((prev) => [
        ...prev,
        {
          name: file.name,
          url: url,
          type: file.type,
        },
      ]);
    });
  };

  const removeUploadedFile = (index: number) => {
    setUploadedFiles((prev) => prev.filter((_, i) => i !== index));
  };

  const downloadFile = (url: string, fileName: string) => {
    // In a real app, this would handle actual file download
    console.log(`Downloading: ${fileName} from ${url}`);
    // Create a temporary download link
    const link = document.createElement("a");
    link.href = url;
    link.download = fileName;
    link.click();
  };

  return (
    <div className="space-y-6">
      {/* Lab Reports Grid */}
      <div className="grid gap-6">
        {labReports.map((report, index) => (
          <motion.div
            key={report.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            className="bg-white rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow"
          >
            {/* Report Header */}
            <div className="p-6 border-b border-gray-100">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <div className="w-12 h-12 bg-gradient-to-r from-[#76B3A8] to-[#5A9B8E] rounded-lg flex items-center justify-center">
                    <FileText className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      {report.name}
                    </h3>
                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                      <Calendar className="w-4 h-4" />
                      <span>{new Date(report.date).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>

                {report.downloadUrl && (
                  <motion.button
                    whileHover={{ scale: 1.05 }}
                    whileTap={{ scale: 0.95 }}
                    onClick={() =>
                      downloadFile(report.downloadUrl!, report.fileName!)
                    }
                    className="flex items-center space-x-2 text-[#76B3A8] hover:text-[#6ba396] transition-colors"
                  >
                    <Download className="w-5 h-5" />
                    <span className="text-sm font-medium">Download</span>
                  </motion.button>
                )}
              </div>
            </div>

            {/* Parameters */}
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {report.parameters.map((param, paramIndex) => (
                  <motion.div
                    key={paramIndex}
                    initial={{ opacity: 0, x: -10 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.1 + paramIndex * 0.05 }}
                    className="flex items-center justify-between p-3 bg-gray-50 rounded-lg"
                  >
                    <div className="flex-1">
                      <p className="text-sm font-medium text-gray-900">
                        {param.name}
                      </p>
                      <p className="text-xs text-gray-500">
                        Range: {param.range}
                      </p>
                    </div>

                    <div className="text-right">
                      <p className="text-sm font-bold text-gray-900">
                        {param.value} {param.unit}
                      </p>
                      <div
                        className={`inline-flex items-center space-x-1 px-2 py-1 rounded-full text-xs font-medium border ${getStatusColor(
                          param.status
                        )}`}
                      >
                        {getStatusIcon(param.status)}
                        <span className="capitalize">{param.status}</span>
                      </div>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Upload Lab Report Section */}
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
        className="bg-white rounded-xl border border-gray-200 shadow-sm"
      >
        <div className="p-6 border-b border-gray-100">
          <div className="flex items-center space-x-3">
            <Upload className="w-6 h-6 text-[#76B3A8]" />
            <h2 className="text-lg font-semibold text-gray-900">
              Upload Lab Report
            </h2>
          </div>
          <p className="text-sm text-gray-600 mt-1">
            Upload your lab reports as PDF or image files
          </p>
        </div>

        <div className="p-6">
          <FileUploader onFilesUploaded={handleFileUpload} />

          {/* Uploaded Files List */}
          {uploadedFiles.length > 0 && (
            <div className="mt-6">
              <h3 className="text-sm font-medium text-gray-900 mb-3">
                Uploaded Files
              </h3>
              <div className="space-y-2">
                {uploadedFiles.map((file, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    className="flex items-center justify-between p-3 bg-green-50 border border-green-200 rounded-lg"
                  >
                    <div className="flex items-center space-x-3">
                      <FileText className="w-5 h-5 text-green-600" />
                      <span className="text-sm font-medium text-green-900">
                        {file.name}
                      </span>
                    </div>

                    <div className="flex items-center space-x-2">
                      <button
                        onClick={() => window.open(file.url, "_blank")}
                        className="p-1 text-green-600 hover:text-green-700 transition-colors"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => downloadFile(file.url, file.name)}
                        className="p-1 text-green-600 hover:text-green-700 transition-colors"
                      >
                        <Download className="w-4 h-4" />
                      </button>
                      <button
                        onClick={() => removeUploadedFile(index)}
                        className="p-1 text-red-600 hover:text-red-700 transition-colors"
                      >
                        <X className="w-4 h-4" />
                      </button>
                    </div>
                  </motion.div>
                ))}
              </div>
            </div>
          )}
        </div>
      </motion.div>
    </div>
  );
};
