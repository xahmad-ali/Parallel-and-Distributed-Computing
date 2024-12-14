import {
	Button,
	FileInput,
	Label,
	Textarea,
	TextInput,
} from "flowbite-react";
import React, { useState } from "react";

function ImageFlies() {
    const [images, setImages] = useState(null);
    const [pattern, setPattern] = useState("");
    const [data, setData] = useState([]);
    const [loading, setLoading] = useState(false);
    const [error, setError] = useState(null);

    // const handleExtract= async(event)=>{
    //     event.preventDefault();
	// 	setLoading(true);

    //     if (!images || images.length === 0 || !pattern.trim()) {
	// 		setLoading(false);
	// 		alert("Please upload files and enter a pattern to search.");
	// 		return;
	// 	}
    //     const lowerCasePattern = pattern.toLowerCase().trim();

    //     const validFiles = Array.from(images).filter((image) =>
    //         ["image/jpeg", "image/png", "image/jpg"].includes(image.type)
    //     );

    //     try {
    //         const formData = new FormData();
    //         validFiles.forEach((image) => formData.append("images", image));
	// 		formData.append("pattern", lowerCasePattern);

	// 		const response = await fetch("http://127.0.0.1:8000/extract-text", {
	// 			method: "POST",
	// 			body: formData,
	// 		});
    //         if (!response.ok) {
	// 			throw new Error(`Server error: ${response.statusText}`);
	// 		}

    //         console.log(response)

    //     } catch (error) {
    //         console.error("Error searching files:", error);
	// 		alert("An error occurred while searching files. Please try again.");
	// 	} finally {
	// 		setLoading(false);
	// 	}
    // }

    const handleExtract = async (event) => {
        event.preventDefault();
        setLoading(true);
    
        if (!images || images.length === 0 || !pattern.trim()) {
            setLoading(false);
            alert("Please upload files and enter a pattern to search.");
            return;
        }
        const lowerCasePattern = pattern.toLowerCase().trim();
    
        const validFiles = Array.from(images).filter((image) =>
            ["image/jpeg", "image/png", "image/jpg"].includes(image.type)
        );
    
        try {
            const formData = new FormData();
            validFiles.forEach((image) => formData.append("files", image)); // Updated to "files"
            formData.append("keywords", lowerCasePattern); // Updated to "keywords"
    
            const response = await fetch("http://127.0.0.1:8000/extract-text", {
                method: "POST",
                body: formData,
            });
    
            if (!response.ok) {
                throw new Error(`Server error: ${response.statusText}`);
            }
    
            const result = await response.json();
            console.log(result)
            setData(Object.entries(result.results));
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
                    <form className="flex flex-col gap-4" onSubmit={handleExtract}>
                        <div>
                            <Label value="Upload excel files" className="m-2" />
                            <div className="flex gap-4">
                                <FileInput
                                    type="file"
                                    accept="image/jpeg, image/png, image/jpg"
                                    required
                                    disabled={loading}
                                    multiple
                                    onChange={(e) => setImages(e.target.files)}
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

{data.length > 0 && (
    <div className="mt-6 p-4 bg-gray-50 border border-gray-200 rounded-lg">
        <h2 className="text-xl font-semibold mb-4">Extracted Data</h2>
        {data.map(([filename, result], index) => (
            <div key={index} className="mb-4">
                <h3 className="font-bold text-gray-700">File: {filename}</h3>
                {result.results.length > 0 ? (
                    <ul className="list-disc pl-5 text-gray-600">
                        {result.results.map((item, i) => (
                            <li key={i}>
                                <strong>Keyword:</strong> {item.keyword} <br />
                                <strong>Line:</strong> {item.line}
                            </li>
                        ))}
                    </ul>
                ) : (
                    <p className="text-gray-500">No matching keywords found.</p>
                )}
            </div>
        ))}
    </div>
)}




            </div>
  )
}

export default ImageFlies