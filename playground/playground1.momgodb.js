/* global use, db */
// MongoDB Playground
// To disable this template go to Settings | MongoDB | Use Default Template For Playground.
// Make sure you are connected to enable completions and to be able to run a playground.
// Use Ctrl+Space inside a snippet or a string literal to trigger completions.
// The result of the last command run in a playground is shown on the results panel.
// By default the first 20 documents will be returned with a cursor.
// Use 'console.log()' to print to the debug output.
// For more documentation on playgrounds please refer to
// https://www.mongodb.com/docs/mongodb-vscode/playgrounds/

// Select the database to use.
use('Sigmadatabase');

// Insert a few documents into the sales collection.
db.getCollection('courses').insertMany([
    [
        {
          "_id": {
            "$oid": "65ea38194820165ff62e102a"
          },
          "userid": "hello20",
          "email": "21102140.advait.desai@gmail.com",
          "password": "gAAAAABl6jgZhwacseWZfZP3_6KYqpuqcfCWxSNJcarU-3pInG6Sg7aEBiTlQNjpUauVbNMGvsyWQAqFyF7AYo6K0Q_PXo_abA==",
          "type": "Employee",
          "date_created": {
            "$date": "2024-03-07T21:56:41.198Z"
          }
        },
        {
          "_id": {
            "$oid": "65ea38194820165ff62e102b"
          },
          "userid": "user123",
          "email": "user123@example.com",
          "password": "gAAAAABl6jgZhwacseWZfZP3_6KYqpuqcfCWxSNJcarU-3pInG6Sg7aEBiTlQNjpUauVbNMGvsyWQAqFyF7AYo6K0Q_PXo_abA==",
          "type": "Customer",
          "date_created": {
            "$date": "2024-03-08T14:20:00.000Z"
          }
        },
        {
          "_id": {
            "$oid": "65ea38194820165ff62e102c"
          },
          "userid": "admin_007",
          "email": "admin@example.com",
          "password": "gAAAAABl6jgZhwacseWZfZP3_6KYqpuqcfCWxSNJcarU-3pInG6Sg7aEBiTlQNjpUauVbNMGvsyWQAqFyF7AYo6K0Q_PXo_abA==",
          "type": "Admin",
          "date_created": {
            "$date": "2024-03-09T09:45:22.123Z"
          }
        }
      ]
      
]);

// Run a find command to view items sold on April 4th, 2014.
const salesOnApril4th = db.getCollection('sales').find({
  date: { $gte: new Date('2014-04-04'), $lt: new Date('2014-04-05') }
}).count();

// Print a message to the output window.
console.log(`${salesOnApril4th} sales occurred in 2014.`);

// Here we run an aggregation and open a cursor to the results.
// Use '.toArray()' to exhaust the cursor to return the whole result set.
// You can use '.hasNext()/.next()' to iterate through the cursor page by page.
db.getCollection('sales').aggregate([
  // Find all of the sales that occurred in 2014.
  { $match: { date: { $gte: new Date('2014-01-01'), $lt: new Date('2015-01-01') } } },
  // Group the total sales for each product.
  { $group: { _id: '$item', totalSaleAmount: { $sum: { $multiply: [ '$price', '$quantity' ] } } } }
]);
