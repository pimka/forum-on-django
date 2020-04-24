<template>
    <div>
        <b-card>
            <b-card-title>{{ heading.head }}</b-card-title>
            <b-card-text>{{ heading.body }}</b-card-text>
            <div v-for="tag in heading.tags" :key="tag">
                <b-badge>{{ tag }}</b-badge>
            </div>
            <b-button v-on:click="visible=true" variant="primary">Edit</b-button>
            <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
            <b-card-group flush :visible="visibleReply">
                <b-card-group-item>
                    <form class="edit">
                        <h4>Edit heading</h4>
                        <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
                            <b-form-input id="inputHead" v-model="heading.head" placeholder="Enter title"/>
                        </b-form-group>
                        <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
                            <b-form-textarea id="inputBody" v-model="heading.body" rows="5"/>
                        </b-form-group>
                        <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
                            <b-form-select v-model="heading.tags" :options="tags" multiple id="inputTags"/>
                        </b-form-group>
                        <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
                    </form>
                </b-card-group-item>
            </b-card-group>
        </b-card>
        <div v-for="mes in item" :key="mes">
            <Messages :item="mes"/>
        </div>
    </div>
</template>

<script>
import { HTTP } from '../../api/common'
import Messages from '../../components/Messages.vue'

export default {
    name: 'Heading',
    components: {
        Messages
    },

    data () {
        return {
            head_uuid: this.$route.params.head_uuid,
            heading: {
                type: Object
            },
            messages: [],
            visible: false,
            tags: []
        }
    },

    created () {
        this.getData()
        this.getMessages(),
        this.getTags()
    },

    methods: {
        getData () {
            HTTP.get(`/headings/${this.head_uuid}/`)
            .then(response => {
                this.heading = response.data
            }).catch(err => { 
                this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
            })
        },
        editData () {
            if (this.validData()) {
                this.visible = false
                HTTP.put(`/headings/${this.head_uuid}/`, this.heading)
                    .then(() => {
                        this.$bvToast.toast('Heading edited', {
                            title: 'Success',
                            variant: 'success'
                        })
                    })
                    .catch(err => { 
                        this.$bvToast.toast(err.message, {
                            title: 'Error',
                            variant: 'danger'
                        })
                    })
            }
        },
        deleteData () {
            HTTP.delete(`/headings/${this.head_uuid}/`)
                .then(() => {
                    this.$bvToast.toast('Heading deleted', {
                        title: 'Success',
                        variant: 'success'
                    })
                    this.$router.push('/')
                })
                .catch(err => { 
                    this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
                })
        },
        validData () {
            if (this.heading.head.length == 0) {
                this.$bvToast.toast('Enter Title', {
                    title: 'Error',
                    variant: 'danger'
                })
            }
        },
        getMessages () {
            HTTP.get('/messages/')
            .then(response => {
                this.messages = response.data
            }).catch(err => { 
                this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
            })
        },
        getTags () {
            HTTP.get('/tags/').then(response => {
                this.tags = response.data
            }).catch(err => { 
                this.$bvToast.toast(err.message, {
                        title: 'Error',
                        variant: 'danger'
                    })
            })
        }
    }
}
</script>