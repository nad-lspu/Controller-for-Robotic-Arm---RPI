export async function getCurrentAngles() {
  try {
    const response = await fetch("http://localhost:8000/gpio/servo-angle");
    if (response.ok) {
      const servoData = await response.json();
      return servoData;
    } else {
      const error = await response.json();
      console.log(JSON.stringify(error));
      return null;
    }
  } catch (error) {
    console.log(JSON.stringify(error));
    return null;
  }
}