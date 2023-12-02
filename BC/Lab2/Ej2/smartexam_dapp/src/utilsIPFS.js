import { create } from 'kubo-rpc-client'
import { Buffer } from "buffer";

async function downloadFileIPFS(cid, container_name, file_name){
    // Connecting to the local IPFS node.
    const client = create('/ip4/127.0.0.1/tcp/5001');
    
    // Getting the exam from IPFS.
    const result = client.cat(cid);
    const chunks = [];
    for await (let res of result) {
      chunks.push(res);
    }
    const buffer = Buffer.concat(chunks);
    // Adjust the type based on the image format.
    const blob = new Blob([buffer], { type: 'image/png' }); 

    // Create an object URL
    const objectURL = URL.createObjectURL(blob);
    // Display the image in an <img> element.
    const examImg = new Image();
    examImg.src = objectURL;
    const imageExamContainer = document.getElementById(container_name);
    if (imageExamContainer) {
      imageExamContainer.appendChild(examImg); // Add the image to the 'div' with ID "imageContainer"
    }
  
    // Downloading the image file, create a link element and trigger the download
    const link = document.createElement('a');
    link.href = objectURL;
    link.download = file_name +'.png'; 
    link.click();
  }

async function uploadFileIPFS(file) {
    console.log("Uploading file to IPFS.")
    const client = create('/ip4/127.0.0.1/tcp/5001')
    // Add file to IPFS.
    const result = await client.add(file);
    // Add file to the local node file system to be able to visualize it.
    await client.files.cp(`/ipfs/${result.cid}`, `/${result.cid}`);
    console.log("File hash:", result.cid);

    return result.cid.toString();
}

export { downloadFileIPFS, uploadFileIPFS };