require('dotenv').config()
const request = require('request-promise')
const API_KEY = process.env.API_KEY 
const PLATFORM = process.env.PLATFORM
const NICKNAME = process.env.NICKNAME
const URL = `https://api.fortnitetracker.com/v1/profile/${PLATFORM}/${NICKNAME}`

const getStatus = async () => {
    let options = {
        uri: URL,
        headers: {
            'TRN-Api-Key': API_KEY
        }
    }

    try {
        let result = await request(options)
        console.log(options)
        console.log(`Result: ${result}`)
    } catch (err) {
        console.log(`Error: ${err}`)
    }
}

const run = async() => {
    await getStatus()
    setTimeout(async () => {
        await run()
    }, 30 * 1000)
}
run()
