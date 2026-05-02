export async function getTime() {
  return {
    success: true,
    time: new Date().toISOString()
  };
}