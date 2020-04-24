<template>
    <div>
            <b-card :header="[item.uuid, item.parent]" :footer="[item.created, item.user_uuid]" :img-scr="item.image">
            <b-card-text>{{ item.body }}</b-card-text>
            <b-card-text>{{ item.file }}</b-card-text>
            <b-button v-on:click="visibleEdit=true" variant="primary">Edit</b-button>
            <b-button v-on:click="deleteData()" variant="danger">Delete</b-button>
            <b-button v-on:click="visibleReply=true" variant="danger">Reply</b-button>
            <b-card-group flush :visible="visibleEdit">
                <b-card-group-item>
                    <form class="edit">
                        <h4>Edit message</h4>
                        <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
                            <b-form-input id="inputBody" v-model="item.body"/>
                        </b-form-group>
                        <b-form-group id="inputFileGroup" label="File" label-for="inputFile">
                            <b-form-file id="inputFile" v-model="item.file" placeholder="Choose a file or drop it here..."/>
                        </b-form-group>
                        <b-form-group id="inputImageGroup" label="Image" label-for="inputImage">
                            <b-form-file id="inputImage" v-model="item.image" placeholder="Choose a image or drop it here..."/>
                        </b-form-group>
                        <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
                    </form>
                </b-card-group-item>
            </b-card-group>
            <b-card-group flush :visible="visibleReply">
                <b-card-group-item>
                    <form class="edit">
                        <h4>Edit message</h4>
                        <b-form-group id="inputBodyGroup" label="Main text" label-for="inputBody">
                            <b-form-input id="inputBody" v-model="new_item.body"/>
                        </b-form-group>
                        <b-form-group id="inputFileGroup" label="File" label-for="inputFile">
                            <b-form-file id="inputFile" v-model="new_item.file" placeholder="Choose a file or drop it here..."/>
                        </b-form-group>
                        <b-form-group id="inputImageGroup" label="Image" label-for="inputImage">
                            <b-form-file id="inputImage" v-model="item.image" placeholder="Choose a image or drop it here..."/>
                        </b-form-group>
                        <b-button type="submit" variant="primary" v-on:click="editData()">Save</b-button>
                    </form>
                </b-card-group-item>
            </b-card-group>
        </b-card>
    </div>
</template>

<script>
import { HTTP } from '../api/common'

export default {
    props: {
        item: {
            type: Object
        }
    },

    data () {
        return {
            visibleEdit: false,
            visibleReply: false,
            new_item: {
                type: Object
            }
        }
    },

    methods: {
        editData () {
            if (this.validData()) {
                this.visibleEdit = false
                HTTP.put(`/messages/${this.item.uuid}/`, this.item)
                    .then(() => {
                        this.$bvToast.toast('Messages edited', {
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
            HTTP.delete(`/messages/${this.item.uuid}/`)
                .then(() => {
                    this.$bvToast.toast('Message deleted', {
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
        },
        replyData () {
            this.visibleReply = false
            this.new_item.parent = this.item.uuid
            if (this.validData()) {
                HTTP.post('/messages/', this.new_item)
                    .then(() => {
                        this.$bvToast.toast('Messages edited', {
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
        validData(){
            return true
        }
    }
}
</script>