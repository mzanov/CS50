document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  document.querySelector('#compose-view').addEventListener('submit', send_email);

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function view_email(email_id){
  fetch(`/emails/${email_id}`)
.then(response => response.json())
.then(email => {
    // Print email
    console.log(email);

    document.querySelector('#emails-view').style.display = 'none';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#email-detail-view').style.display = 'block';

    document.querySelector('#email-detail-view').innerHTML = `

    <h3>${email.subject}</h3>
    <div class="row">
      <div class="d-flex flex-column col-8">
        <span><strong>From:</strong> ${email.sender}</span>
        <span><strong>To:</strong> ${email.recipients}</span>
        <span><strong>Timestamp:</strong> ${email.timestamp}</span>
      </div>

      <div class="col-4 d-flex justify-content-end">
        <div>
          <div class="btn-group" role="group">
            <button class="btn btn-sm btn-outline-primary" id="reply">Reply</button>
            <button class="btn btn-sm btn-outline-primary" id="archive">Archive</button>
          </div>
        </div>
      </div>
    </div>

    <hr>

    <div>${email.body}</div>
    `
    document.querySelector('#archive').innerHTML = email.archived ? "Unarchive" : "Archive";
    document.querySelector('#archive').className = email.archived ? "btn btn-success" : "btn btn-danger";

    document.querySelector('#archive').addEventListener('click',function(){
      fetch(`/emails/${email.id}`, {
        method: 'PUT',
        body: JSON.stringify({
            archived: !email.archived
        })
      })
      .then(() => {load_mailbox('archive')})
    })

    document.querySelector('#reply').className = "btn btn-info";

    document.querySelector('#reply').addEventListener('click',function(){
      compose_email();
      
      document.querySelector("#compose-recipients").value = email.sender;
      let subject = email.subject;
      if(subject.split(' ',1)[0] != "Re:"){
        subject = "Re: " + email.subject;
      }
      document.querySelector("#compose-subject").value = subject;
      document.querySelector("#compose-body").value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}`;
    })




    if(email.read){
    fetch(`/emails/${email.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: true
      })
    })
  }



    // ... do something else with email ...
});
}

function load_mailbox(mailbox) {
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-detail-view').style.display = 'none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    // Print emails
    emails.forEach(email => {
      const newEmail = document.createElement('div');

      newEmail.className ='border-style';
      
      newEmail.innerHTML = `
      <h6>Sender: ${email.sender}</h6>
      <h6>Subject: ${email.subject}</h6>
      <p>${email.timestamp}<p>
      `;

      newEmail.className = email.read ? 'read' : 'unread';
      newEmail.addEventListener('click', function() {
        view_email(email.id);
      });


      document.querySelector('#emails-view').append(newEmail);
      

    });

    // ... do something else with emails ...
});
}

function send_email(event){
  
  event.preventDefault();
  console.log('HELLOO!!');

  const recipients = document.querySelector("#compose-recipients").value;
  const subject = document.querySelector("#compose-subject").value;
  const body = document.querySelector("#compose-body").value;

  fetch("/emails", {
    method: "POST",
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body,
    }),
})
    .then((response) => response.json())
    .then((result) => {
        console.log(result);
        load_mailbox("sent");
    });
}
