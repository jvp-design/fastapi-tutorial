<script>
async function getData() {
    const res = await fetch("http://localhost:8000/blah")
    const data = await res.json()

    if (res.ok) {
        return data
    } else {
        throw new Error(data)
    }
}

let promise = getData()

const handleClick = () => {
    promise = getData()
}
</script>

<h1>Welcome to SvelteKit</h1>
<p>Visit <a href="https://kit.svelte.dev">kit.svelte.dev</a> to read the documentation</p>

<button on:click={handleClick}>
  Get Data
</button>

{#await promise}
  <p>...waiting</p>
{:then data}
  <p>Data is {data.hello}</p>
{:catch error}
  <p>Error is {error}</p>
{/await}
