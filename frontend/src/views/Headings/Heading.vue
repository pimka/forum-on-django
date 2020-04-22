<template>
    <div>
        <b-jumbotron>
            <template v-slot:lead>{{ head }}</template>
            <hr class="my-4">
            <p>{{ body }}</p>
            <div v-for="tag in tags" :key="tag">
                <b-badge>{{ tag }}</b-badge>
            </div>
            <b-button v-on:click="editData()" variant="primary">Edit</b-button>
            <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
        </b-jumbotron>
    </div>
</template>