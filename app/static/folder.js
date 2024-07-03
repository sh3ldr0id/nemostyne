import { initializeApp } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-app.js';
import { getFirestore, collection, doc, getDoc } from 'https://www.gstatic.com/firebasejs/10.12.2/firebase-firestore.js';

const firebaseConfig = {
    apiKey: "AIzaSyCfaVQ7rQJQ1-2dNrj1rvBaMtVQqTL_n6I",
    authDomain: "nemostyne-core.firebaseapp.com",
    projectId: "nemostyne-core",
    storageBucket: "nemostyne-core.appspot.com",
    messagingSenderId: "574915725086",
    appId: "1:574915725086:web:1170b007f88358564beb0f",
    measurementId: "G-GNN7MH6RYY"
};

const app = initializeApp(firebaseConfig);
const db = getFirestore();

const foldersCollection = collection(db, "folders");
const filesCollection = collection(db, "files");

const FOLDERS = {{ folders | tojson }};
const FILES = {{ files | tojson }};

const foldersElement = document.getElementById("folders");
const filesElement = document.getElementById("files");

async function createFolder() {
    const folderName = document.getElementById('folderName').value.trim();
    if (!folderName) {
        alert('Please enter a folder name.');
        return;
    }

    let user = firebase.auth().currentUser;
    if (!user) {
        alert('User not authenticated.');
        return;
    }

    const userId = user.uid;
    const currentFolderId = ""; 
    const created = new Date();

    const folderData = {
        "previous": currentFolderId,
        "name": folderName,
        "files": [],
        "folders": [],
        "created": created,
        "by": userId
    };

    try {
        const response = await fetch('/create-folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(folderData)
        });

        if (response.ok) {
            alert('Folder created successfully.');
            location.reload();
        } else {
            alert('Failed to create folder.');
        }
    } catch (error) {
        console.error('Error creating folder:', error);
        alert('An error occurred while creating the folder.');
    }
}

function getIcon(filename) {
    const ext = filename.split('.').pop().toLowerCase();
    if (['gif', 'png', 'jpg', 'jpeg', 'bmp', 'svg', 'webp'].includes(ext)) {
        return 'image';
    } else if (['mp4', 'mov', 'avi', 'mkv', 'flv', 'wmv', 'webm'].includes(ext)) {
        return 'video';
    } else if (['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt'].includes(ext)) {
        return 'file-alt';
    } else {
        return 'file';
    }
}

function truncateName(name) {
    return name.length > 9 ? name.slice(0, 9) + "..." : name;
}

async function fetchThumbnail(docId) {
    try {
        const response = await fetch(`/thumbnail/${docId}`);
        if (response.ok && response.redirected === false) {
            const blob = await response.blob();
            return URL.createObjectURL(blob);
        }
    } catch (error) {
        return null;
    }
    return null;
}

function formatDateTime(date) {
    date = new Date(date.seconds * 1000 + Math.floor(date.nanoseconds / 1000000));

    const year = date.getFullYear();
    const month = String(date.getMonth() + 1).padStart(2, '0');
    const day = String(date.getDate()).padStart(2, '0');
    const hours = String(date.getHours()).padStart(2, '0');
    const minutes = String(date.getMinutes()).padStart(2, '0');
    const seconds = String(date.getSeconds()).padStart(2, '0');

    return `${year}-${month}-${day} ${hours}:${minutes}:${seconds}`;
}

if (FOLDERS.length == 0) foldersElement.innerHTML = `<p>No folders available.</p>`;
if (FILES.length == 0) filesElement.innerHTML = `<p>No files available.</p>`;

async function getFolders() {
    for (const folderID of FOLDERS) {
        const docRef = doc(foldersCollection, folderID);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            const data = docSnap.data();

            foldersElement.innerHTML += `
                <ul class="list-group shadow flex-row align-items-center">
                    <a href="/folder/${docSnap.id}" class="list-group-item list-group-item-action d-flex align-items-center text-decoration-none text-reset border-0">
                        <i class="fa-solid fa-folder me-3" style="font-size: 2rem;"></i>
                        <div>
                            <p class="text-body-primary mb-0">${truncateName(data.name)}</p>
                            <small class="text-body-secondary">${formatDateTime(data.created)}</small>
                        </div>
                    </a>
                    <i class="fa-solid fa-link mx-3" onclick="copyLink('/folder/${docSnap.id}')"></i>
                </ul>
            `;
        }
    }
}

async function getFiles() {
    for (const fileID of FILES) {
        const docRef = doc(filesCollection, fileID);
        const docSnap = await getDoc(docRef);

        if (docSnap.exists()) {
            const data = docSnap.data();

            const icon = getIcon(data.name);
            var iconHtml = `
            <div class="card-img-top d-flex justify-content-center align-items-center">
                <i class="fa-solid fa-${icon}" style="font-size: 6rem;"></i>
            </div>`;

            if (["image", "video"].includes(icon)) {
                const thumbnailUrl = await fetchThumbnail(docSnap.id);

                if (thumbnailUrl) {
                    iconHtml = `<img src="${thumbnailUrl}" alt="thumbnail" class="card-img-bottom">`;
                }
            }

            filesElement.innerHTML += `
                <div class="card">
                    <div class="card-body m-0 py-1 d-flex justify-content-between align-items-center">
                        <div style="overflow: hidden;">
                            <a href="/file/${docSnap.id}" class="card-title text-decoration-none mb-0 p-0">${truncateName(data.name)}</a> <br>
                            <small class="text-body-secondary flex-1">450.65Mb</small> 
                        </div>
                        <i class="fa-solid fa-link ps-2" onclick="copyLink('/file/${docSnap.id}')"></i>
                    </div>
                    ${iconHtml}
                </div>
            `;
        }
    }
}

getFolders();
getFiles();