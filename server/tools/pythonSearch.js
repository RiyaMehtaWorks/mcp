import axios from "axios";

export async function pythonSearch({ query, state, crop }) {
  const res = await axios.post("http://127.0.0.1:56789/search", {
    query,
    state,
    crop
  });

  return {
    tool: "pythonSearch",
    data: res.data
  };
}