<template>
    <div>
        <b-form @submit="sendData">
            <h3>Create Heading</h3>
            <b-form-group id="inputHeadGroup" label="Title" label-for="inputHead">
                <b-form-input id="inputHead" v-model="head" placeholder="Enter title"/>
            </b-form-group>
            <b-form-group id="inputBodyGroup" label="Main Text" label-for="inputBody">
                <b-form-textarea id="inputBody" v-model="body" rows="5"/>
            </b-form-group>
            <b-form-group id="inputTagsGroup" label="Select Tags" label-for="inputTags">
                <b-form-select v-model="selected" :options="tags" multiple id="inputTags"/>
            </b-form-group>
            <b-button type="submit" variant="primary">Create</b-button>
            <b-alert v-for="err in createErrors" :key="err" show dismissible fade variant="danger">{{ err }}</b-alert>
            <b-alert v-if="isSuccess" show dismissible fade variant="success">Created</b-alert>
        </b-form>
    </div>
</template>

<script>
import { HTTP } from '../../api/common'

export default {
    data () {
        return {
            head: '',
            body: '',
            selected: [],
            tags: [],
            createErrors: [],
            isSuccess: false
        }
    },

    created () {
        this.getJSON()
    },

    methods: {
        sendData () {
            if (this.validData()) {
                HTTP.post('/headings/', {
                    'header': this.head,
                    'body': this.body,
                    'tags': this.selected
                }).then(response => {
                    this.items = response.data
                    this.err = ''
                    this.isSuccess = true
                }).catch(err => { this.createErrors.push(err.message) })
            }
        },
        validData () {
            this.createErrors = []
            if (this.selected.length == 0) {
                this.createErrors.push('Select tag')
                return false
            } else {
                return true
            }
        },
        getJSON () {
            HTTP.get('/tags/').then(response => {
                this.tags = response.data
                console.log(response.data)
            }).catch(err => { this.createErrors.push(err.message) })
        }
    }
}
</script>