const randomstring = require('randomstring');
const username = randomstring.generate();
const email = `${username}@test.com`;


describe('Login', () => {
    it('should display the sign in form', () => {
      cy
        .visit('/login')
        .get('h1').contains('Login')
        .get('form');
    });

    it('should allow a user to sign in', () => {
        cy
          .visit('/register')
          .get('input[name="username"]').type(username)
          .get('input[name="email"]').type(email)
          .get('input[name="password"]').type('test')
          .get('input[type="submit"]').click()
    
        // log a user out
        cy.get('.navbar-burger').click();
        cy.contains('Log Out').click();

        // log a user in
        cy
          .get('a').contains('Log In').click()
          .get('input[name="email"]').type(email)
          .get('input[name="password"]').type('test')
          .get('input[type="submit"]').click()
          .wait(100);

        // assert user is redirect to '/'
        // assert '/' is displayed properly
        cy.contains('All Users');

        cy
          .get('table')
          .find('tbody > tr').last()
          .find('td').contains(username);
        cy.get('.navbar-burger').click();
        cy.get('.navbar-menu').within(() => {
          cy
            .get('.navbar-item').contains('User Status')
            .get('.navbar-item').contains('Log Out')
            .get('.navbar-item').contains('Log In').should('not.be.visible')
            .get('.navbar-item').contains('Register').should('not.be.visible');
        });

    });
});