import axios from "axios";

export async function pythonPing() {
  const res = await axios.get("http://127.0.0.1:56789/ping");

  return {
    tool: "pythonPing",
    data: res.data
  };
}