import {
	Button,
	FileInput,
	Label,
	Table,
	Textarea,
	TextInput,
} from "flowbite-react";
import React, { useState } from "react";
import * as XLSX from "xlsx";

const ExcelFiles = () => {
	const [files, setFiles] = useState(null);
	const [pattern, setPattern] = useState("");
	const [data, setData] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState(null);

	// const handleSearch = async (event) => {
	// 	event.preventDefault();
	// 	setLoading(true);
	// 	setError(null);
	  
	// 	if (!files || files.length === 0 || !pattern.trim()) {
	// 	  setLoading(false);
	// 	  alert("Please upload files and enter a pattern to search.");
	// 	  return;
	// 	}
	  
	// 	const lowerCasePattern = pattern.toLowerCase().trim();
	  
	// 	const validFiles = Array.from(files).filter((file) => 
	// 		["application/vnd.ms-excel",
	// 		 "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
	// 		 "text/csv", 
	// 		 "application/csv", 
	// 		 "application/x-csv"
	// 		].includes(file.type)
	// 	);
	  
	// 	if (validFiles.length === 0) {
	// 	  setLoading(false);
	// 	  alert("No valid Excel files found. Please upload .xls or .xlsx files.");
	// 	  return;
	// 	}
	  
	// 	try {
	// 	  // Prepare form data for API call
	// 	  const formData = new FormData();
	// 	  validFiles.forEach((file) => formData.append("files", file));
	// 	  formData.append("pattern", lowerCasePattern);
	  
	// 	  // API call to backend with improved error handling
	// 	  const response = await fetch("http://127.0.0.1:8000/search", {
	// 		method: "POST",
	// 		body: formData,
	// 		// Add CORS headers
	// 		headers: {
	// 			// No additional headers needed for FormData
	// 			'Accept': 'application/json'
	// 		}
	// 	  });
	  
	// 	  if (!response.ok) {
	// 		// Try to parse error message from server
	// 		const errorText = await response.text();
	// 		throw new Error(`Server error: ${errorText || response.statusText}`);
	// 	  }
	  
	// 	  // Check content type to determine how to parse response
	// 	  const contentType = response.headers.get("content-type");
	// 	  let searchResults;
		  
	// 	  if (contentType && contentType.includes("application/json")) {
	// 		// If JSON response
	// 		searchResults = await response.json();
	// 	  } else if (contentType && contentType.includes("application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")) {
	// 		// If Excel file response
	// 		// const blob = await response.blob();
	// 		// You might want to handle Excel file download here
	// 		searchResults = [];
	// 	  } else {
	// 		throw new Error("Unexpected response type");
	// 	  }
	  
	// 	  if (searchResults.length === 0) {
	// 		alert("No matches found for the given pattern.");
	// 	  }
	  
	// 	  // Process results 
	// 	  const processedResults = validFiles.map(file => ({
	// 		fileName: file.name,
	// 		headers: searchResults.length > 0 ? Object.keys(searchResults[0]) : null,
	// 		matches: searchResults.map((result, index) => ({
	// 		  rowIndex: index + 1,
	// 		  rowData: Object.values(result)
	// 		}))
	// 	  }));
	  
	// 	  setData((prevData) => [
	// 		{
	// 		  pattern: pattern.trim(),
	// 		  files: validFiles.map((file) => file.name),
	// 		  searchResults: processedResults,
	// 		},
	// 		...prevData,
	// 	  ]);
	// 	} catch (error) {
	// 	  console.error("Error searching files:", error);
	// 	  setError(error.message);
	// 	  alert(`An error occurred while searching files: ${error.message}`);
	// 	} finally {
	// 	  setLoading(false);
	// 	}
	// };

	// // Add a method to handle file download
	// const handleDownload = (dataObject) => {
	// 	// Implement download logic here
	// 	console.log("Download data:", dataObject);
	// };

	const handleSearch = async (event) => {
		event.preventDefault();
		setLoading(true);
	
		if (!files || files.length === 0 || !pattern.trim()) {
			setLoading(false);
			alert("Please upload files and enter a pattern to search.");
			return;
		}
	
		const lowerCasePattern = pattern.toLowerCase().trim(); // No splitting into an array
	
		const validFiles = Array.from(files).filter((file) =>
			[
				"application/vnd.ms-excel",
				"application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
				"text/csv",
				"application/csv",
				"application/x-csv",
			].includes(file.type)
		);
	
		if (validFiles.length === 0) {
			setLoading(false);
			alert("No valid Excel files found. Please upload .xls, .xlsx, or .csv files.");
			return;
		}
	
		try {
			const formData = new FormData();
			validFiles.forEach((file) => formData.append("files", file));
			formData.append("pattern", lowerCasePattern);
	
			const response = await fetch("http://127.0.0.1:8000/search", {
				method: "POST",
				body: formData,
			});
	
			if (!response.ok) {
				throw new Error(`Server error: ${response.statusText}`);
			}
	
			// Trigger file download for the StreamingResponse
			const blob = await response.blob();
			const url = window.URL.createObjectURL(blob);
			const link = document.createElement("a");
			link.href = url;
			link.setAttribute("download", "search_results.xlsx");
			document.body.appendChild(link);
			link.click();
			link.remove();
			alert("File downloaded successfully.");
		} catch (error) {
			console.error("Error searching files:", error);
			alert("An error occurred while searching files. Please try again.");
		} finally {
			setLoading(false);
		}
	};
	
	return (
		<div className="w-full bg-cover bg-center bg-fixed bg-no-repeat 
			bg-[url('../../light.jpg')] dark:bg-[url('../../dark.jpg')]">
			<div className="max-w-4xl my-10 mx-3 p-3 sm:mx-12 lg:mx-auto sm:p-10 self-center dark:shadow-whiteLg
			bg-transparent border-2 border-white/40 dark:border-white/20 backdrop-blur-[30px] rounded-lg shadow-xl bg-white bg-opacity-35 dark:bg-transparent dark:bg-opacity-100">
				<h1 className="text-center text-3xl mb-7 font-semibold uppercase">
					Data Searching in Excel Files
				</h1>
				<form className="flex flex-col gap-4" onSubmit={handleSearch}>
					<div>
						<Label value="Upload excel files" className="m-2" />
						<div className="flex gap-4">
							<FileInput
								type="file"
								accept=".xls, .xlsx, .csv"
								required
								disabled={loading}
								multiple
								onChange={(e) => setFiles(e.target.files)}
								className="w-full sm:w-auto flex-auto"
							/>
						</div>
					</div>
					<div>
						<Label value="Enter anything to search" className="m-2" />
						<Textarea
							type="text"
							placeholder="Enter keywords separated by spaces or commas"
							rows={2}
							value={pattern}
							disabled={loading}
							required
							id="pattern"
							className="flex-1"
							onChange={(e) => setPattern(e.target.value)}
						/>
					</div>
					<Button
						type="submit"
						gradientDuoTone="purpleToPink"
						outline
						disabled={loading}
						className="focus:ring-1 uppercase">
						{loading ? "Processing... Please wait!" : "Search"}
					</Button>
				</form>
			</div>
			
			{error && (
				<div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role="alert">
					{error}
				</div>
			)}
			
			{data.length > 0 &&
				data.map((dataObject, index) => (
					<div key={index} className="mt-5">
						{dataObject.searchResults.map((result, resultIndex) => (
							<div key={resultIndex} className="mt-5">
								<div>
									<h4 className="text-sm text-center mt-2 mb-5">
										Search Results in <span className="font-semibold">{result.fileName}</span>
									</h4>
									<Table hoverable>
										<Table.Head className="sticky top-[60px] z-10">
											<Table.HeadCell>Row Number</Table.HeadCell>
											{result.headers && 
												result.headers.map((header, headerIndex) => (
													<Table.HeadCell key={headerIndex}>{header}</Table.HeadCell>
												))
											}
										</Table.Head>
										<Table.Body>
											{result.matches.map((match, matchIndex) => (
												<Table.Row key={matchIndex}>
													<Table.Cell>{match.rowIndex}</Table.Cell>
													{match.rowData.map((cell, cellIndex) => {
														const cellContent = cell.toString();
														const highlightedContent = cellContent
															.split(new RegExp(`(${dataObject.pattern})`, "gi"))
															.map((part, i) =>
																part.toLowerCase() === dataObject.pattern.toLowerCase() ? (
																	<span
																		key={i}
																		className="bg-yellow-100 dark:bg-yellow-800"
																	>
																		{part}
																	</span>
																) : (
																	part
																)
															);
														return (
															<Table.Cell key={cellIndex}>
																{highlightedContent}
															</Table.Cell>
														);
													})}
												</Table.Row>
											))}
										</Table.Body>
									</Table>
								</div>
							</div>
						))}
						
						<div className="flex justify-between mt-10">
							<span>
								Click the "Download" button to save the search results as an Excel file.
							</span>
							<Button
								type="button"
								gradientDuoTone="purpleToBlue"
								size="sm"
								onClick={() => handleDownload(dataObject)}
								outline
								className="focus:ring-1 w-full sm:w-28">
								Download
							</Button>
						</div>
					</div>
				))
			}
		</div>
	);
}

export default ExcelFiles;