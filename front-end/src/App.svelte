<script>
  import { onMount } from "svelte";
  let tasks = [];
  let selectedTodo;
  let newTaskContent = "";
  let editContent = "";
  let editModalOpen = false;
  let deleteModalOpen = false;

  const loadTasks = async () => {
    const response = await fetch("http://localhost:81/tasks");
    const data = await response.json();
    tasks = data.data;
  };

  onMount(async () => {
    loadTasks();
  });

  const addTodo = async () => {
    if (!newTaskContent) {
      alert("Inserisci un contenuto");
      return;
    }
    const response = await fetch("http://localhost:81/tasks", {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: newTaskContent,
        id: crypto.randomUUID(),
      }),
    });
    const data = await response.json();
    await loadTasks();
    newTaskContent = "";
  };

  const markDone = async (task) => {
    const response = await fetch(`http://localhost:81/tasks/${task[0]}`, {
      method: "PATCH",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        content: task[1],
        done: !task[2],
      }),
    });
    const data = await response.json();
    await loadTasks();
  };

  const editTodo = async () => {
    const response = await fetch(
      `http://localhost:81/tasks/${selectedTodo[0]}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          content: editContent,
          done: selectedTodo[2],
        }),
      }
    );
    const data = await response.json();
    await loadTasks();
    editModalOpen = false;
  };

  const deleteTodo = async () => {
    const response = await fetch(
      `http://localhost:81/tasks/${selectedTodo[0]}`,
      {
        method: "DELETE",
      }
    );
    const data = await response.json();
    await loadTasks();
    deleteModalOpen = false;
  };
</script>

<div class="bg-base-100 flex items-center justify-center min-h-screen">
  <div
    class="bg-base-300 flex flex-col justify-center items-center p-8 rounded-lg gap-y-5"
  >
    <h1 class="text-2xl font-bold">To do list</h1>
    <div class="form-control">
      <div class="input-group">
        <input
          type="text"
          placeholder="Nuova task"
          bind:value={newTaskContent}
          class="input input-bordered"
        />
        <button on:click={addTodo} class="btn btn-square btn-secondary">
          <h2>+</h2>
        </button>
      </div>
    </div>
    <ul class="flex flex-col w-max">
      {#each tasks as task}
        <li class="flex w-64 gap-x-5 justify-start items-center">
          <p class="px-2 bg-base-100 border rounded border-stone-600 w-3/5">
            {task[1]}
          </p>
          <input
            type="checkbox"
            bind:checked={task[2]}
            on:click={() => markDone(task)}
            class="toggle toggle-primary w-1/5"
          />
          <div class="dropdown w-1/5">
            <label tabindex="0" class="btn m-1 btn-xs"
              ><svg
                class="fill-secondary"
                width="16px"
                height="16px"
                viewBox="0 0 16 16"
                xmlns="http://www.w3.org/2000/svg"
                ><path
                  d="M13.8 2.2a2.51 2.51 0 0 0-3.54 0l-6.9 6.91-1.76 3.62a1.26 1.26 0 0 0 1.12 1.8 1.23 1.23 0 0 0 .55-.13l3.62-1.76 6-6 .83-.82.06-.06a2.52 2.52 0 0 0 .02-3.56zm-.89.89a1.25 1.25 0 0 1 0 1.77l-1.77-1.77a1.24 1.24 0 0 1 .86-.37 1.22 1.22 0 0 1 .91.37zM2.73 13.27 4.29 10 6 11.71zm4.16-2.4L5.13 9.11 10.26 4 12 5.74z"
                /></svg
              ></label
            >
            <ul
              tabindex="0"
              class="dropdown-content menu p-2 shadow bg-base-100 rounded-box w-52"
            >
              <li>
                <button
                  on:click={() => {
                    editContent = task[1];
                    selectedTodo = task;
                    editModalOpen = true;
                  }}>modifica</button
                >
              </li>
              <li>
                <button
                  on:click={() => {
                    selectedTodo = task;
                    deleteModalOpen = true;
                  }}>cancella</button
                >
              </li>
            </ul>
          </div>
        </li>
      {/each}
    </ul>
  </div>
</div>

{#if editModalOpen}
  <div class="modal modal-open  ">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Modifica elemento</h3>
      <input
        type="text"
        bind:value={editContent}
        class="input input-bordered"
      />
      <div class="modal-action">
        <div on:click={() => (editModalOpen = false)} class="btn btn-ghost">
          Annulla
        </div>
        <div on:click={editTodo} class="btn">Modifica</div>
      </div>
    </div>
  </div>
{/if}

{#if deleteModalOpen}
  <div class="modal modal-open  ">
    <div class="modal-box">
      <h3 class="font-bold text-lg">Sei sicuro di voler eliminare la task?</h3>
      <div class="modal-action">
        <div on:click={() => (deleteModalOpen = false)} class="btn btn-ghost">
          Annulla
        </div>
        <div on:click={deleteTodo} class="btn btn-error">Elimina</div>
      </div>
    </div>
  </div>
{/if}
