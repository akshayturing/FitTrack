from app import db
from datetime import datetime

class RevokedToken(db.Model):
    __tablename__ = 'revoked_tokens'
    __table_args__ = {'extend_existing': True}
    id = db.Column(db.Integer, primary_key=True)
    jti = db.Column(db.String(120), nullable=False, unique=True)
    revoked_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=False)
    
    @classmethod
    def is_token_revoked(cls, jti):
        """Check if the given token is revoked"""
        return cls.query.filter_by(jti=jti).first() is not None
    
    @classmethod
    def revoke_token(cls, jti, expires_at):
        """Revoke a token"""
        revoked_token = cls(jti=jti, expires_at=expires_at)
        db.session.add(revoked_token)
        db.session.commit()
    
    @classmethod
    def prune_expired_tokens(cls):
        """Remove expired tokens from blacklist to prevent DB bloat"""
        now = datetime.utcnow()
        expired = cls.query.filter(cls.expires_at < now).delete()
        db.session.commit()
        return expired
    
    def __repr__(self):
        return f"<RevokedToken {self.jti}>"
