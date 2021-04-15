from flask import Blueprint, render_template, request, flash, jsonify, abort
from flask_login import login_required, current_user
# from .models import Note
from .models import Board
from . import db
import json
from .models import User

views = Blueprint('views', __name__)


@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        board_content = request.form.get('board.content')
        board_title = request.form.get('board.title')

        if len(board_content) < 1:
            flash('Board is too short!', category='error')
        if len(board_title) < 1:
            flash('Board is too short!', category='error')
        
        else:
            new_board = Board(content=board_content, user_id=current_user.id, title = board_title)
            
            db.session.add(new_board)
            db.session.commit()
            flash('Board added!', category='success')

    return render_template("home.html", user=current_user)


@views.route('/delete-board', methods=['POST'])
def delete_board():
    board = json.loads(request.data)
    boardId = board['boardId']
    board = Board.query.get(boardId)
    if board:
        if board.user_id == current_user.id:
            db.session.delete(board)
            db.session.commit()

    return jsonify({})


@views.route("/<int:id>", methods=["PUT", "PATCH"], endpoint="update")
def board_update(id):

    pass

    #Update a board
    board_fields = board_schema.load(request.json)
    user_id = get_jwt_identity()

    user = User.query.get(user_id)

    if not user:
        return abort(401, description="Invalid user")

    boards = Board.query.filter_by(id=id, user_id=user.id)
    
    if boards.count() != 1:
        return abort(401, description="Unauthorized to update this board")

    boards.update(board_fields)
    db.session.commit()

    #return jsonify(board_schema.dump(boards[0]))
    return render_template("boards_index.html", boards=boards[0])