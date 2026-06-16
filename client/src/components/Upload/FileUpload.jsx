import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

export default function FileUpload() {
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const onDrop = useCallback(async (acceptedFiles, rejectedFiles) => {
    if (rejectedFiles.length > 0) {
      setError('Only CSV files are accepted (max 10MB)');
      return;
    }
    if (acceptedFiles.length === 0) return;
    setError('');
    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', acceptedFiles[0]);
      const res = await axios.post('/api/upload', formData, {
        headers: { 'Content-Type': 'multipart/form-data' },
      });
      navigate(`/analysis/${res.data.id}`);
    } catch (err) {
      setError(err.response?.data?.message || 'Upload failed. Please try again.');
    } finally {
      setUploading(false);
    }
  }, [navigate]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'text/csv': ['.csv'] },
    maxFiles: 1,
    maxSize: 10 * 1024 * 1024,
    disabled: uploading,
  });

  return (
    <div className="w-full max-w-2xl mx-auto">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-2xl p-12 text-center cursor-pointer transition-all duration-200 ${
          isDragActive
            ? 'border-brand-500 bg-brand-500/10'
            : 'border-slate-700 hover:border-slate-500 bg-slate-900/50'
        } ${uploading ? 'opacity-60 cursor-not-allowed' : ''}`}
      >
        <input {...getInputProps()} />
        <div className="text-5xl mb-4">{uploading ? '⏳' : isDragActive ? '📂' : '📁'}</div>
        {uploading ? (
          <div>
            <p className="text-white font-semibold text-lg mb-1">Analyzing your data...</p>
            <p className="text-slate-400 text-sm">Running AI analysis, this may take a moment</p>
            <div className="mt-4 flex justify-center">
              <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin" />
            </div>
          </div>
        ) : isDragActive ? (
          <p className="text-brand-400 font-semibold text-lg">Drop your CSV here</p>
        ) : (
          <div>
            <p className="text-white font-semibold text-lg mb-1">Drop your CSV file here</p>
            <p className="text-slate-400 text-sm mb-4">or click to browse</p>
            <span className="inline-block bg-brand-500 hover:bg-brand-600 text-white text-sm font-medium px-5 py-2 rounded-lg transition-colors">
              Choose file
            </span>
            <p className="text-slate-600 text-xs mt-4">CSV only · Max 10MB</p>
          </div>
        )}
      </div>
      {error && (
        <div className="mt-3 bg-red-900/30 border border-red-800 text-red-300 px-4 py-3 rounded-lg text-sm">
          {error}
        </div>
      )}
    </div>
  );
}
