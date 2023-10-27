const customDate = new Date(2023, 11, 31, 12, 0, 0, 0); // Año: 2023, Mes: diciembre (0-based), Día: 31, Hora: 11:00:00
const currentUnixTimestamp = Math.floor(Date.now() / 1000); // Get the current Unix timestamp
const newUnixTimestamp = currentUnixTimestamp + 300; // Add 5 minutes (300 seconds) 

console.log("\nCurrent Unix Timestamp:", currentUnixTimestamp);
console.log("Current Timestamp:", new Date(currentUnixTimestamp*1000));
console.log("Unix Timestamp + 5 minutes:", newUnixTimestamp);
