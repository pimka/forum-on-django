<template>
    <div>
        <h3>Top headings</h3>
        <b-table :fields="fields" :items="items" head-variant="light" :striped="true">
        </b-table>
    </div>
</template>

<script>
export default {
    data () {
        return {
            fields: [
                { key: 'header', label: 'Heading' },
                { key: 'views', label: 'Views' },
                { key: 'created', label: 'Created' },
            ]
        }
    },

    props: {
        items: {
            type: Array
        }
    }
}
</script>