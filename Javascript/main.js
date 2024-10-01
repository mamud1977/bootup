console.log('Hi...')

let greeting = 'Hello '
let name = prompt('Your name?')

document.getElementById('greeting').innerHTML = greeting+ name

let animals = ['Tiger', 'Elephant', 'Zebra','Ostrich']

console.log(animals[0])

animals[4] = 'Horse'


for (let i=0; i<5; i++)
{
    console.log(animals[i])

}

document.getElementById('animal').innerHTML = animals

let score = parseInt(prompt('What is your math schore? '))

let grade = 0

if (score >= 90) { alert('Excellent') }
else if (score >= 80) { alert('Good') }
else { alert('Poor') }





